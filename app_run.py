from vk_bot import Bot
from data.config import token, group_id
from utils.info_logging import configure_logging


if __name__ == "__main__":
    configure_logging()
    bot = Bot(group_id=group_id, token=token)
    bot.run()