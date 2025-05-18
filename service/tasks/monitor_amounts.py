import asyncio
from service.utils import get_amounts_data
from service.storage.money_storage import money_storage
from service.storage.rates_storage import rates_storage

import logging

logger = logging.getLogger("monitor_amounts")
logger_console = logging.getLogger("console")

async def monitor_amounts():
    logger.info("Start monitor_amounts")
    prev_amounts = money_storage.get_amounts().copy()
    prev_rates = rates_storage.get_rates().copy()

    while True:
        current_amounts = money_storage.get_amounts().copy()
        current_rates = rates_storage.get_rates().copy()

        if current_amounts != prev_amounts or current_rates != prev_rates:
            diff_mess = "The exchange rate or balance of funds has changed"
            logger.info(diff_mess)
            amounts_data = get_amounts_data()
            logger_console.info(diff_mess)
            logger_console.info(amounts_data)

        prev_amounts = current_amounts
        prev_rates = current_rates

        await asyncio.sleep(60)