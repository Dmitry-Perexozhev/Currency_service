import httpx
import requests

from abc import ABC, abstractmethod
from typing import Dict, Set

from service.config import RATES_PROVIDERS_URLS
from service.storage.money_storage import money_storage

from service.logging_config import get_logger
logger = get_logger(__name__, "provider.log")

class RatesProvider(ABC):
    @abstractmethod
    async def fetch_rates(self) -> Dict[str, float]:
        pass


class CBRRatesProvider(RatesProvider):
    def __init__(self):
        self.url = RATES_PROVIDERS_URLS["cbr"]

    async def fetch_rates(self) -> Dict[str, float]:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.url)
            response.raise_for_status()
            logger.debug(f"Response status by {self.url}: {response.status_code}")
            data = response.json()
        valute = data.get("Valute", {})
        currencies = money_storage.get_amounts().keys()
        rates = {}
        for cur in currencies:
            if cur == 'rub':
                rates['rub'] = 1.0
            else:
                valute_code = cur.upper()
                value = valute.get(valute_code, {}).get("Value")
                if value is None:
                    error_msg = f"Rate for currency '{valute_code}' not found in service response."
                    logger.error(error_msg)
                    raise ValueError(error_msg)
                rates[cur] = value
        logger.debug(f"Get current exchange rates from the provider {rates}")
        return rates


def fetch_available_currencies(url: str) -> Set[str]:
    response = requests.get(url)
    response.raise_for_status()
    logger.debug(f"Response status for fetch_available_currencies: {response.status_code}")
    data = response.json()

    valutes = data.get("Valute", {})
    return {code.lower() for code in valutes.keys()}