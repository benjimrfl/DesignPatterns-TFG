import logging

def setup_logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("api_logger")
    return logger
