import httpx
import logging
from typing import Dict
import asyncio
from service.storage import RatesStorage
from service.provider import CBRRatesProvider
logger = logging.getLogger('rates_fetcher')


async def get_rates(rate_storage: RatesStorage, period: int) -> Dict[str, float]:
    logger.info(f"Запущена фоновая задача получения курсов валют с периодичностью {period} минут.")
    provider = CBRRatesProvider()
    while True:
        logger.debug("Начало нового цикла получения курсов.")
        print("Начало нового цикла получения курсов.")
        try:
            rates = await provider.fetch_rates()
            print("rates")
            rate_storage.set_rates(rates)
            logger.info(f"Курсы обновлены: {rates}")
        except Exception as e:
            logger.error(f"Ошибка при получении курсов валют: {e}")
        await asyncio.sleep(period * 60)