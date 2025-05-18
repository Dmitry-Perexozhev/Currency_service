from typing import Dict

from service.config import RATES_PROVIDERS_URLS
from service.provider import fetch_available_currencies
from service.storage import money_storage, rates_storage

def get_amounts_data() -> Dict:
    usd = money_storage.get_amount("usd")
    eur = money_storage.get_amount("eur")
    rub = money_storage.get_amount("rub")

    rates = rates_storage.get_rates()
    rub_usd = rates.get('usd', 0.0)
    rub_eur = rates.get('eur', 0.0)
    print(rates)

    usd_eur = rub_usd / rub_eur if rub_eur else 0.0

    total_rub = usd * rub_usd + eur * rub_eur + rub
    total_usd = total_rub / rub_usd if rub_usd else 0.0
    total_eur = total_rub / rub_eur if rub_eur else 0.0

    return {
        **money_storage.get_amounts(),
        **rates_storage.get_rates()
        # "rub": rub,
        # "usd": usd,
        # "eur": eur,
        # "rub-usd": rub_usd,
        # "rub-eur": rub_eur,
        # "usd-eur": usd_eur,
        # "sum": {
        #     "rub": round(total_rub, 2),
        #     "usd": round(total_usd, 2),
        #     "eur": round(total_eur, 2)
        # }
    }

def is_valid_currency(cur: str) -> bool:
    available_currencies = fetch_available_currencies(RATES_PROVIDERS_URLS["cbr"])
    return cur in available_currencies