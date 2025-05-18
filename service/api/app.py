from fastapi import FastAPI, HTTPException

from service.api.middleware import log_requests
from service.api.lifespan import lifespan
from service.storage.money_storage import money_storage
from service.utils import get_amounts_data
from service.logging_config import get_logger

logger = get_logger(__name__, "api.log")

app = FastAPI(lifespan=lifespan)
app.middleware("http")(log_requests)


@app.get("/amount/get")
async def get_amounts():
    amounts_data = get_amounts_data()
    logger.info(f"Get amounts: {amounts_data}")
    return amounts_data


@app.get("/{currency}/get")
async def get_currency_amount(currency: str):
    currency = currency.lower()
    if currency not in money_storage.get_amounts().keys():
        logger.warning(f"Attempt to access unsupported currency: {currency}")
        raise HTTPException(status_code=404, detail="Currency not supported")
    logger.info(f"Get amount for currency: {currency.upper()}")
    return {
        "name": currency.upper(),
        "value": money_storage.get_amount(currency)
    }


@app.post("/amount/set")
async def set_amounts(amounts: dict):
    money_storage.set_amounts(amounts)
    logger.info(f"Set mounts: {amounts}")
    return {"message": "Amounts set successfully"}


@app.post("/modify")
async def modify_amounts(changes: dict):
    money_storage.modify_amounts(changes)
    logger.info(f"Modify amounts: {changes}")
    return {"message": "Amounts modified successfully"}