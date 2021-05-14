import logging

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