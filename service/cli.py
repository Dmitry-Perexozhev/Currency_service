import argparse
import logging

from service.utils import is_valid_currency

logger = logging.getLogger("cli")
logger_console = logging.getLogger("console")


def parse_debug_flag(value: str) -> bool:
    true_values = {'1', 'true', 'True', 'y', 'Y'}
    false_values = {'0', 'false', 'False', 'n', 'N'}
    if value in true_values:
        return True
    elif value in false_values:
        return False
    else:
        raise argparse.ArgumentTypeError(f"Unsupported value debug: {value}")


def parse_args():
    parser = argparse.ArgumentParser(description="Asynchronous currency service")

    parser.add_argument(
        '--period',
        type=int,
        required=True,
        help='Exchange rate request period in minutes'
    )

    parser.add_argument(
        '--debug',
        type=parse_debug_flag,
        nargs='?',
        const=True,
        default=False,
        help='Debug mode (true/false/1/0/y/n)'
    )

    known_args, unknown_args = parser.parse_known_args()

    balances = {}
    i = 0
    while i < len(unknown_args):
        arg = unknown_args[i]

        if arg.startswith("--"):
            currency = arg[2:].lower()
            try:
                value = float(unknown_args[i + 1])
            except (IndexError, ValueError):
                msg = f"The currency {currency} does not have a valid numeric value."
                logger.error(msg)
                raise ValueError(msg)
            if is_valid_currency(currency):
                balances[currency] = value
            else:
                msg = f"Unknown currency {currency}"
                logger.warning(msg)
                logger_console.warning(msg)
            i += 2
        else:
            msg = "Invalid argument format"
            logger.error(msg)
            raise ValueError(msg + ". Enter arguments in the form --currency value. Example --usd 1000")

    if not balances:
        logger.error("No currency specified")
        raise ValueError("You must specify at least one currency with an amount, for example: --usd 1000")

    result = {
        "period": known_args.period,
        "debug": known_args.debug,
        "balances": balances,
    }

    logger.info(f"Command line arguments: {result}")
    return result
