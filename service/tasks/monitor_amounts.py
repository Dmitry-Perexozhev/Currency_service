import asyncio
from service.utils import get_amounts_data
from service.storage.money_storage import money_storage
from service.storage.rates_storage import rates_storage
from service.logging_config import get_logger
logger = get_logger(__name__, "monitor_amounts.log")

async def monitor_amounts():
    prev_amounts = None
    prev_rates = None

    while True:
        current_amounts = money_storage.get_amounts().copy()
        current_rates = rates_storage.get_rates().copy()

        if prev_amounts is not None and prev_rates is not None:
            if current_amounts != prev_amounts or current_rates != prev_rates:
                logger.info("The exchange rate or balance of funds has changed")
                output = get_amounts_data()
                print(output)

        prev_amounts = current_amounts
        prev_rates = current_rates

        await asyncio.sleep(60)