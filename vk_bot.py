import requests
import vk_api
import logging

from pony.orm import db_session
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from _token import token, group_id
from models import UserState, Registration
from setting import SCENARIO,INTENTS,DEFAULT_ANSWER
import handler

# log_obj = logging.getLogger('VK_LOG')
# log_obj.setLevel(logging.INFO)
# fh = logging.FileHandler('log_vk.log', 'w', 'UTF-8')
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
# log_obj.addHandler(fh)

log_obj = logging.getLogger('VK_BOT')
def configure_logging():

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S"))
    stream_handler.setLevel(logging.DEBUG)
    log_obj.addHandler(stream_handler)

    file_handler = logging.FileHandler(filename='bot.log', mode='a', encoding='UTF-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S"))
    file_handler.setLevel(logging.DEBUG)
    log_obj.addHandler(file_handler)

    log_obj.setLevel(logging.DEBUG)


class Bot:

    def __init__(self, group_id: int, token: str):
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log_obj.exception("Error handling event")

    @db_session
    def on_event(self, event):

        if event.type != VkBotEventType.MESSAGE_NEW:
            log_obj.info('I dont know how to work with this event %s', event.type)
            return
        #user_id = event.object.peer_id
        user_id = event.object.message['from_id']
        text = event.message.text
        state = UserState.get(user_id=str(user_id))

        if state is not None:
            # continiue scenario
            self.continue_scenario(text=text, state=state, user_id=user_id)
        else:
            # search intent
            for intent in INTENTS:
                log_obj.debug(f'User gets {intent}')
                if any(token in text.lower() for token in intent['tokens']):
                    # run intent
                    if intent['answer']:
                        self.send_text(text_to_send=intent['answer'], user_id=user_id)
                    else:
                        self.start_scenario(scenario_name=intent['scenario'], user_id=user_id, text=text)
                    break
            else:
                self.send_text(text_to_send=DEFAULT_ANSWER, user_id=user_id)


    def send_text(self, text_to_send, user_id):
        self.api.messages.send(
            message=text_to_send,
            random_id=random.randint(0, 2 ** 20),
            peer_id=user_id
        )

    def send_image(self, image, user_id):
        upload_url = self.api.photos.getMessagesUploadServer()['upload_url']
        upload_data = requests.post(url=upload_url, files={'photo': ('image.png', image, 'image/png')}).json()
        image_data = self.api.photos.saveMessagesPhoto(**upload_data)
        owner_id, media_id = image_data[0]['owner_id'], image_data[0]['id']
        attachment = f'photo{owner_id}_{media_id}'
        self.api.messages.send(
            attachment=attachment,
            random_id=random.randint(0, 2 ** 20),
            peer_id=user_id
        )

    def send_step(self, step, user_id, text, context):
        if 'text' in step:
            self.send_text(text_to_send=step['text'].format(**context), user_id=user_id)
        if 'image' in step:
            handlers = getattr(handler, step['image'])
            image = handlers(text, context)
            self.send_image(image=image, user_id=user_id)

    def start_scenario(self, scenario_name, user_id, text):
        scenario = SCENARIO[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        self.send_step(step=scenario['steps'][first_step], user_id=user_id, text=text, context={})
        UserState(scenario_name=scenario_name,
                    step_name=first_step,
                    context={},
                    user_id=str(user_id)
                )

    def continue_scenario(self, text, state, user_id):
        steps = SCENARIO[state.scenario_name]['steps']
        step = steps[state.step_name]

        handlers = getattr(handler, step['handler'])
        if handlers(text=text, context=state.context):
            # next step
            next_step = steps[step['next_step']]
            self.send_step(next_step, user_id, text, state.context)
            if next_step['next_step']:
                # switch to next step
                state.step_name = step['next_step']
            else:
                # finish scenario
                log_obj.info('User registration info: {name} {email}'.format(**state.context))
                Registration(name=state.context['name'], email=state.context['email'])
                state.delete()
        else:
            # retry current step
            text_to_send = step['failure_text'].format(**state.context)
            self.send_text(text_to_send=text_to_send, user_id=user_id)


if __name__ == "__main__":
    configure_logging()
    bot = Bot(group_id=group_id, token=token)
    bot.run()



