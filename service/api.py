from fastapi import FastAPI, HTTPException, Request
from .storage import rates_storage, config_storage, money_storage
from service.tasks.rates_fetcher import get_rates
from service.utils import get_amounts_data
from service.tasks.monitor_amounts import monitor_amounts
import asyncio
from service.logging_config import get_logger
logger = get_logger(__name__, "api.log")


async def lifespan(app: FastAPI):
    logger.info("Starting background task to fetch rates.")
    print("Starting background task to fetch rates.")
    task_rates = asyncio.create_task(
        get_rates(
            rates_storage,
            config_storage.get_period()
        )
    )
    task_monitor = asyncio.create_task(monitor_amounts())
    yield
    task_rates.cancel()
    task_monitor.cancel()
    logger.info("Background task cancelled.")

app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    if config_storage.get_debug():
        body = await request.body()
        print(f"\n[DEBUG] Request: {request.method} {request.url}")
        print(f"Headers: {dict(request.headers)}")
        print(f"Body: {body.decode() if body else 'No body'}\n")

    response = await call_next(request)

    if config_storage.get_debug():
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        async def fake_body_iterator():
            yield response_body

        response.body_iterator = fake_body_iterator()
        print(f"[DEBUG] Response status: {response.status_code}")
        print(f"Body: {response_body.decode()}\n")

    return response

@app.get("/amount/get")
async def get_amounts():
    return get_amounts_data()

@app.get("/{currency}/get")
async def get_currency_amount(currency: str):
    currency = currency.lower()
    if currency not in {"usd", "eur", "rub"}:
        logger.warning(f"Attempt to access unsupported currency: {currency}")
        raise HTTPException(status_code=404, detail="Currency not supported")
    logger.info(f"Fetching amount for currency: {currency.upper()}")
    return {
        "name": currency.upper(),
        "value": money_storage.get_amount(currency)
    }


@app.post("/amount/set")
async def set_amounts(amounts: dict):
    money_storage.set_amounts(amounts)
    logger.info(f"Amounts set: {amounts}")
    return {"message": "Amounts set successfully"}


@app.post("/modify")
async def modify_amounts(changes: dict):
    money_storage.modify_amounts(changes)
    logger.info(f"Amounts modified: {changes}")
    return {"message": "Amounts modified successfully"}