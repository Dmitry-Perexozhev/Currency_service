from abc import ABC, abstractmethod
from typing import Dict
import httpx
from service.config import RATES_PROVIDERS_URLS

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
            data = response.json()

        valute = data.get("Valute", {})
        return {
            "usd": valute.get("USD", {}).get("Value"),
            "eur": valute.get("EUR", {}).get("Value"),
            "rub": 1.0,
        }
