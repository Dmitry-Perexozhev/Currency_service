from itertools import combinations
from typing import Dict

from service.provider import fetch_available_currencies
from service.rates_url import RATES_PROVIDERS_URLS
from service.storage.money_storage import money_storage
from service.storage.rates_storage import rates_storage


def get_amounts_data() -> Dict:
    amounts = money_storage.get_amounts()
    rates = rates_storage.get_rates()

    result = {f"rub-{cur}": rate for cur, rate in rates.items()}

    result.update({
        f"{base}-{quote}": round(rates[base] / rates[quote], 4)
        for base, quote in combinations(rates, 2)
    })

    total_rub = sum(amounts[cur] * rates[cur] for cur in amounts)
    total = {"rub": round(total_rub, 2)}

    total.update({
        cur: round(total_rub / rate, 2)
        for cur, rate in rates.items()
        if cur != "rub" and rate != 0
    })

    result["sum"] = total

    return {**amounts, **result}


def is_valid_currency(cur: str) -> bool:
    available_currencies = fetch_available_currencies(RATES_PROVIDERS_URLS["cbr"])
    return cur in available_currencies
