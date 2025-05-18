import asyncio
import logging
from service.utils import get_amounts_data
from service.storage import money_storage, rates_storage
logger = logging.getLogger('amount_logger')

async def monitor_amounts():
    prev_amounts = None
    prev_rates = None

    while True:
        current_amounts = money_storage.get_amounts().copy()
        current_rates = rates_storage.get_rates().copy()

        if prev_amounts is not None and prev_rates is not None:
            # Сравниваем текущие и предыдущие данные
            if current_amounts != prev_amounts or current_rates != prev_rates:
                output = get_amounts_data()
                print(f"Изменения в балансах или курсах:\n{output}")

        prev_amounts = current_amounts
        prev_rates = current_rates

        await asyncio.sleep(60)