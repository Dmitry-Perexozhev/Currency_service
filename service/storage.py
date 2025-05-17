from typing import Dict
from service.logging_config import get_logger

logger = get_logger(__name__, "storage.log")


class MoneyStorage:
    def __init__(self):
        self._amounts: Dict[str, float] = {}

    def get_amount(self, currency: str) -> float:
        amount = self._amounts.get(currency.lower(), 0.0)
        logger.debug(f"Получено значение {amount} для валюты {currency.upper()}")
        return amount

    def set_amounts(self, values: Dict[str, str]) -> None:
        for k, v in values.items():
            self._amounts[k.lower()] = float(v)
        logger.info(f"Установлены новые значения: {self._amounts}")

    def modify_amounts(self, delta: Dict[str, str]) -> None:
        for k, v in delta.items():
            k = k.lower()
            self._amounts[k] = self._amounts.get(k, 0.0) + float(v)
        logger.info(f"Изменены значения: {self._amounts}")


class RatesStorage:
    def __init__(self):
        self._course: Dict[str, float] = {}

    def set_rates(self, course: Dict[str, float]):
        for k, v in course.items():
            self._course[k] = v
        logger.info(f"Обновлены курсы валют: {self._course}")

    def get_rates(self) -> Dict[str, float]:
        logger.debug(f"Получены курсы валют: {self._course}")
        return self._course


class ConfigStorage:
    def __init__(self):
        self._config: Dict[str, int | bool] = {}
        self._config["period"] = 5
        self._config["debug"] = False

    def set_config(self, period: int, debug: bool):
        self._config["period"] = period
        self._config["debug"] = debug
        logger.info(f"Установлена конфигурация: period={period}, debug={debug}")

    def get_period(self) -> int:
        return self._config["period"]

    def get_debug(self) -> bool:
        return self._config["debug"]


money_storage = MoneyStorage()
rates_storage = RatesStorage()
config_storage = ConfigStorage()