# Usage example:
# from hestia_logger import setup_logger
# logger = setup_logger(__name__)
# logger.info(" Started logging")


import logging

LOG_TO_FILE = True  # Set to False to disable file logging
LOG_FILE_PATH = 'logs.log'  # Path to the log file
LOG_TO_COLSOLE = True  # Set to False to disable console logging


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:  
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        if LOG_TO_FILE:
            file_handler = logging.FileHandler(str(LOG_FILE_PATH))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        if LOG_TO_COLSOLE:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

    return logger
