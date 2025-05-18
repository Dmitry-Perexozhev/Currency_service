import logging
from logging.config import dictConfig

import uvicorn

from service.api.app import app
from service.cli import parse_args
from service.logging_config import LOGGING_CONFIG
from service.storage.config_storage import config_storage
from service.storage.money_storage import money_storage

dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("main")
logger_console = logging.getLogger("console")


def main():
    start_mes = "Start currency service app"

    config = parse_args()

    logger.info(start_mes) if config['debug']\
        else logger_console.info(start_mes)

    money_storage.set_amounts(config['balances'])

    balance_mes = f"Setting initial balance values: {config['balances']}"
    logger.info(balance_mes) if config['debug'] \
        else logger_console.info(balance_mes)

    config_storage.set_config(config["period"], config["debug"])
    logger.info(f"Rate update period: {config['period']} min."
                f" Debug mode: {config['debug']}")

    logger.info("Launch FastAPI application")
    uvicorn.run(app, host="127.0.0.1", port=8000, lifespan="on")


if __name__ == "__main__":
    main()
