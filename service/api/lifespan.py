import asyncio
from fastapi import FastAPI


from service.storage.config_storage import config_storage
from service.tasks.rates_fetcher import get_rates
from service.tasks.monitor_amounts import monitor_amounts

import logging

logger = logging.getLogger("lifespan")


async def lifespan(app: FastAPI):
    logger.info("Starting background task to fetch rates.")
    task_rates = asyncio.create_task(
        get_rates(config_storage.get_period())
    )
    logger.info("Starting background task to monitor amounts.")
    task_monitor = asyncio.create_task(monitor_amounts())
    yield
    task_rates.cancel()
    task_monitor.cancel()
    logger.info("Background tasks cancelled.")

