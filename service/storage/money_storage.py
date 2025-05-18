import logging
from typing import Dict

logger = logging.getLogger("money_storage")


class MoneyStorage:
    def __init__(self):
        self._amounts: Dict[str, float] = {}

    def get_amount(self, currency: str) -> float:
        amount = self._amounts.get(currency.lower(), 0.0)
        logger.debug(f"Get {amount} for {currency.upper()}")
        return amount

    def get_amounts(self):
        return self._amounts

    def set_amounts(self, values: Dict[str, str]) -> None:
        for k, v in values.items():
            self._amounts[k.lower()] = float(v)
            logger.info(f"Set new value for {k} = {v}")

    def modify_amounts(self, delta: Dict[str, str]) -> None:
        for k, v in delta.items():
            k = k.lower()
            self._amounts[k] = self._amounts.get(k, 0.0) + float(v)
            logger.info(f"Modify value for {k} to {v}")


money_storage = MoneyStorage()
