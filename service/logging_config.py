import logging
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # Важно: не отключать uvicorn и другие
    "formatters": {
        "default": {
            "format": "[{asctime}] {levelname} | {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file_main": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": os.path.join(LOG_DIR, "main.log"),
            "encoding": "utf-8",
        },
        "file_api": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": os.path.join(LOG_DIR, "api.log"),
            "encoding": "utf-8",
        },
        "file_storage": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": os.path.join(LOG_DIR, "storage.log"),
            "encoding": "utf-8",
        },
        "file_tasks": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": os.path.join(LOG_DIR, "tasks.log"),
            "encoding": "utf-8",
        },
        "file_cli": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": os.path.join(LOG_DIR, "cli.log"),
            "encoding": "utf-8",
        },
        "file_provider": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": os.path.join(LOG_DIR, "provider.log"),
            "encoding": "utf-8",
        },

    },
    "loggers": {
        "main": {
            "handlers": ["file_main"],
            "level": "DEBUG",
            "propagate": False,
        },
        "app": {
            "handlers": ["file_main", "file_api"],
            "level": "DEBUG",
            "propagate": False,
        },
        "lifespan": {
            "handlers": ["file_main", "file_api"],
            "level": "DEBUG",
            "propagate": False,
        },
        "config_storage": {
            "handlers": ["file_main", "file_storage"],
            "level": "DEBUG",
            "propagate": False,
        },
        "money_storage": {
            "handlers": ["file_main", "file_storage"],
            "level": "DEBUG",
            "propagate": False,
        },
        "rates_storage": {
            "handlers": ["file_main", "file_storage"],
            "level": "DEBUG",
            "propagate": False,
        },
        "monitor_amounts": {
            "handlers": ["file_main", "file_tasks"],
            "level": "DEBUG",
            "propagate": False,
        },
        "rates_fetcher": {
            "handlers": ["file_main", "file_tasks"],
            "level": "DEBUG",
            "propagate": False,
        },
        "cli": {
            "handlers": ["file_main", "file_cli"],
            "level": "DEBUG",
            "propagate": False,
        },
        "provider": {
            "handlers": ["file_main", "file_provider"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
