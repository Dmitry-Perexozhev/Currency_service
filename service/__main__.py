from service import api
from .cli import parse_args
from .storage import money_storage, config_storage
import asyncio
import uvicorn
from .api import app
from service.logging_config import get_logger
logger = get_logger(__name__, "__main__.log")

def main():
    config = parse_args()

    money_storage.set_amounts(config['balances'])
    logger.info(f"Установлены начальные балансы: {config['balances']}")

    config_storage.set_config(config["period"], config["debug"])
    logger.info(f"Период обновления курса: {config['period']} мин. Режим отладки: {config['debug']}")

    logger.info("Запуск FastAPI приложения на http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()