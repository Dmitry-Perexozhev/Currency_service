import httpx
import logging
from typing import Dict
from .storage import RatesStorage
import asyncio

logger = logging.getLogger(__name__)

async def get_rates(rate_storage: RatesStorage, period: int) -> Dict[str, float]:
    URL = "https://www.cbr-xml-daily.ru/daily_json.js"
    while True:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(URL)
                response.raise_for_status()
                data = response.json()

            valute = data.get("Valute", {})
            rates = {
                "usd": valute.get("USD", {}).get("Value"),
                "eur": valute.get("EUR", {}).get("Value"),
                "rub": 1.0,
            }
            rate_storage.set_rates(rates)
            print(f"Курсы обновлены: {rates}")
        except Exception as e:
            logger.error(f"Ошибка при получении курсов валют: {e}")
        await asyncio.sleep(period * 60)