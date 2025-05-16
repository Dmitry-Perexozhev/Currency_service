from typing import Dict


class MoneyStorage:
    def __init__(self):
        self._amounts: Dict[str, float] = {}

    def get_amount(self, currency: str) -> float:
        return self._amounts.get(currency.lower(), 0.0)

    def set_amounts(self, values: Dict[str, str]) -> None:
        for k, v in values.items():
            self._amounts[k.lower()] = float(v)

    def modify_amounts(self, delta: Dict[str, str]) -> None:
        for k, v in delta.items():
            k = k.lower()
            self._amounts[k] = self._amounts.get(k, 0.0) + float(v)


class RatesStorage:
    def __init__(self):
        self._course: Dict[str, float] = {}

    def set_rates(self, course: Dict[str, float]):
        for k, v in course.items():
            self._course[k] = v


    def get_rates(self) -> Dict[str, float]:
        return self._course


class ConfigStorage:
    def __init__(self):
        self._config: Dict[str, int | bool] = {}

    def set_config(self, period: int, debug: bool):
        self._config["period"] = period
        self._config["debug"] = debug

    def get_config(self, config_name: str) -> bool | int:
        return self._config[config_name]


money_storage = MoneyStorage()
rates_storage = RatesStorage()
config_storage = ConfigStorage()