import asyncio
import logging
from typing import Dict

from service.provider import CBRRatesProvider
from service.storage.config_storage import config_storage
from service.storage.rates_storage import rates_storage

logger = logging.getLogger("rates_fetcher")
logger_console = logging.getLogger("console")


async def get_rates(period: int) -> Dict[str, float]:
    logger.info(f"Run a background task to get exchange rates every {period} minutes.")
    provider = CBRRatesProvider()
    logger.info(f"Set provider {provider.__class__.__name__}")
    while True:
        logger.debug("Start of a new cycle of receiving rates")
        try:
            rates = await provider.fetch_rates()
            if not rates:
                logger.warning("Received empty rates dictionary.")
                continue
            success_fetch_mes = f"Successfully fetched exchange rates: {rates}"
            logger.info(success_fetch_mes) if config_storage.get_debug() \
                else logger_console.info(success_fetch_mes)
            rates_storage.set_rates(rates)
            logger.info(f"Rates updated in storage: {rates}")

        except Exception as e:
            logger.error(f"Error while getting exchange rates: {e}")

        await asyncio.sleep(period * 60)
