from vk_bot import configure_logging, Bot
from data.config import token, group_id


if __name__ == "__main__":
    configure_logging()
    bot = Bot(group_id=group_id, token=token)
    bot.run()