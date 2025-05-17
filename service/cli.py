import argparse
from service.logging_config import get_logger
logger = get_logger(__name__, "cli.log")

def str2bool(value: str) -> bool:
    true_values = {'1', 'true', 'True', 'y', 'Y'}
    false_values = {'0', 'false', 'False', 'n', 'N'}
    if value in true_values:
        return True
    elif value in false_values:
        return False
    else:
        raise argparse.ArgumentTypeError(f"Неподдерживаемое значение debug: {value}")


def parse_args():
    parser = argparse.ArgumentParser(description="Асинхронный валютный сервис")

    parser.add_argument('--period', type=int, required=True, help='Период запроса курса валют в минутах')

    parser.add_argument('--debug', type=str2bool, nargs='?', const=True, default=False,
                        help='Режим отладки (true/false/1/0/y/n)')


    known_currencies = {'usd', 'rub', 'eur'}
    for currency in known_currencies:
        parser.add_argument(f'--{currency}', type=float, help=f'Начальная сумма для {currency.upper()}')

    args = parser.parse_args()

    balances = {}
    for currency in known_currencies:
        amount = getattr(args, currency)
        if amount is not None:
            balances[currency] = amount

    if not balances:
        logger.error("Не указана ни одна валюта")
        raise ValueError("Нужно указать хотя бы одну валюту: --usd, --rub или --eur")

    result = {
        "period": args.period,
        "debug": args.debug,
        "balances": balances,
    }

    logger.info(f"Аргументы командной строки: {result}")
    return result