from abc import ABC, abstractmethod
from typing import Dict, Set
import httpx
from service.config import RATES_PROVIDERS_URLS
import requests

from service.storage import money_storage


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
            data = await response.json()

        valute = data.get("Valute", {})
        currencies = money_storage.get_amounts.keys()
        print(currencies)
        rates = {}
        for cur in currencies:
            if cur == 'rub':
                rates['rub'] = 1.0
            else:
                api_code = cur.upper()
                value = valute.get(api_code, {}).get("Value")
                if value is None:
                    error_msg = f"Курс для валюты '{cur}' не найден в ответе сервиса."
                    # logger.error(error_msg)
                    raise ValueError(error_msg)
                rates[cur] = value
        return rates

def fetch_available_currencies(url: str) -> Set[str]:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    valutes = data.get("Valute", {})
    return {code.lower() for code in valutes.keys()}