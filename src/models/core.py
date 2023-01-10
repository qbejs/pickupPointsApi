import os
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Dict, Union


class HealthcheckResponse(BaseModel):
    id: UUID
    timestamp: datetime
    system_status: str
    connection_details: Union[dict, None] = None


class LogConfig(BaseModel):

    LOGGER_NAME: str = os.getenv("LOGGER_NAME")
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL")

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        os.getenv('LOGGER_NAME'): {"handlers": ["default"], "level": LOG_LEVEL},
    }
