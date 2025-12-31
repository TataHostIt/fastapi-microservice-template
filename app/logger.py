import datetime
import json
import logging
import os
import socket
from typing import Any

PROFILE = os.getenv('PROFILE', "dv")


class LogEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        elif isinstance(obj, (set, frozenset)):
            return tuple(obj)
        elif isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        return super().default(obj)


class StructuredMessage:
    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    def __str__(self) -> str:
        return LogEncoder().encode(self.kwargs)


class OnelineFormatter(logging.Formatter):
    COLORS = {
        "grey": "\x1b[90m",
        "red": "\x1b[91m",
        "green": "\x1b[92m",
        "yellow": "\x1b[93m",
        "blue": "\x1b[94m",
        "magenta": "\x1b[95m",
        "cyan": "\x1b[96m",
        "white": "\x1b[97m",
        "reset": "\x1b[0m",
    }

    def formatException(self, exc_info: Any) -> str:
        result = super().formatException(exc_info)
        return repr(result)

    def format(self, record: logging.LogRecord) -> str:
        if PROFILE == "pr-disabled":
            result = super().format(record)
            if record.exc_text:
                result = result.replace("\n", "")
            result_dict = record.__dict__
            result_dict["host"] = socket.gethostname()
            msg = str(StructuredMessage(**result_dict))
        else:
            msg = record.getMessage()

        # Pick color from record or fall back to logger
        color = getattr(record, 'color', None) or getattr(record.__dict__.get('logger', None), 'color', None)
        if not color:
            color = getattr(logging.getLogger(record.name), 'color', None)

        if color in self.COLORS:
            return f"{self.COLORS[color]}{msg}{self.COLORS['reset']}"
        return msg


class StructuredLogger:
    DEFAULT_LEVEL = "DEBUG"

    @staticmethod
    def create_logger(name: str = __name__, color: str = None) -> logging.Logger:
        logger = logging.getLogger(name)

        if not logger.handlers:  # ✅ Prevent adding duplicate handlers
            log_handler = logging.StreamHandler()
            formatter = OnelineFormatter(datefmt="%Y-%m-%d %H:%M:%S")
            log_handler.setFormatter(formatter)
            logger.addHandler(log_handler)

        logger.setLevel(os.getenv("LOG_LEVEL", StructuredLogger.DEFAULT_LEVEL).upper())
        logger.color = color
        logger.propagate = False

        return logger



logger = StructuredLogger.create_logger()
