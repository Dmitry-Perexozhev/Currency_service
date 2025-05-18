from typing import Dict

import logging

logger = logging.getLogger("rates_storage")



class RatesStorage:
    def __init__(self):
        self._course: Dict[str, float] = {}

    def set_rates(self, course: Dict[str, float]):
        for k, v in course.items():
            self._course[k] = v
        logger.info(f"Set exchange rate: {self._course}")

    def get_rates(self) -> Dict[str, float]:
        logger.debug(f"Get exchange rate: {self._course}")
        return self._course


rates_storage = RatesStorage()
