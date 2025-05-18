import logging
from typing import Dict

logger = logging.getLogger("config_storage")


class ConfigStorage:

    def __init__(self):
        self._config: Dict[str, int | bool] = {"period": 5, "debug": False}

    def set_config(self, period: int, debug: bool):
        self._config["period"] = period
        self._config["debug"] = debug
        logger.debug(f"Set configuration: {self._config}")

    def get_period(self) -> int:
        logger.debug(f"Get period: {self._config["period"]}")
        return self._config["period"]

    def get_debug(self) -> bool:
        logger.debug(f"Get period: {self._config["debug"]}")
        return self._config["debug"]


config_storage = ConfigStorage()
