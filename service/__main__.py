from service import api
from .cli import parse_args
from .storage import money_storage, config_storage
import asyncio
import uvicorn
from .api import app


def main():
    config = parse_args()
    money_storage.set_amounts(config['balances'])
    config_storage.set_config(config["period"], config["debug"])
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()