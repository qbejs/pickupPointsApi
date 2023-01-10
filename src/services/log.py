import logging
import os
from logging.config import dictConfig
from dotenv import load_dotenv
from src.models.core import LogConfig

load_dotenv()


def logger():
    dictConfig(LogConfig().dict())
    return logging.getLogger(os.getenv("LOGGER_NAME"))
