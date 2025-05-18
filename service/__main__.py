import uvicorn

from service.cli import parse_args
from service.storage.money_storage import money_storage
from service.storage.config_storage import config_storage
from service.api.app import app


from logging.config import dictConfig
from service.logging_config import LOGGING_CONFIG
dictConfig(LOGGING_CONFIG)
import logging

logger = logging.getLogger("main")


def main():
    logger.info(f"Start currency service app")

    config = parse_args()

    money_storage.set_amounts(config['balances'])
    logger.info(f"Setting initial balance values: {config['balances']}")

    config_storage.set_config(config["period"], config["debug"])
    logger.info(f"Rate update period: {config['period']} min. Debug mode: {config['debug']}")


    logger.info("Launch FastAPI application")
    uvicorn.run(app, host="127.0.0.1", port=8000, lifespan="on")


if __name__ == "__main__":
    main()