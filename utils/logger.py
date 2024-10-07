import logging
import os
import time
from enum import Enum


class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]


class Logger(metaclass=Singleton):
    def __init__(self, log_lvl=LogLevel.INFO):
        self._log = logging.getLogger("selenium")
        self._log.setLevel(LogLevel.DEBUG.value)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.log_file = self._create_log_file()
        self._configure_logging(log_lvl, formatter)

    def _create_log_file(self):
        current_time = time.strftime("%Y-%m-%d")
        log_directory = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../tests", "logs")
        )

        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        return os.path.join(log_directory, f"log_{current_time}.log")

    def _configure_logging(self, log_lvl, formatter):
        fh = logging.FileHandler(self.log_file, mode="w")
        fh.setFormatter(formatter)
        fh.setLevel(log_lvl.value)
        self._log.addHandler(fh)

    def get_instance(self):
        return self._log
