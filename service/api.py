from fastapi import FastAPI, HTTPException, Request
from .storage import rates_storage, config_storage, money_storage
from .rates_fetcher import get_rates
import asyncio
from service.logging_config import get_logger
logger = get_logger(__name__, "api.log")

async def lifespan(app: FastAPI):
    logger.info("Starting background task to fetch rates.")
    task = asyncio.create_task(
        get_rates(
            rates_storage,
            config_storage.get_period()
        )
    )
    yield
    task.cancel()
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
    logger.info("Fetching all amounts and calculating totals.")

    usd = money_storage.get_amount("usd")
    eur = money_storage.get_amount("eur")
    rub = money_storage.get_amount("rub")

    rub_usd = rates_storage.get_rates()['usd']
    rub_eur = rates_storage.get_rates()['eur']

    usd_eur = rub_usd / rub_eur if rub_eur else 0.0

    total_rub = usd * rub_usd + eur * rub_eur + rub
    total_usd = total_rub / rub_usd if rub_usd else 0.0
    total_eur = total_rub / rub_eur if rub_eur else 0.0

    return {
        "rub": rub,
        "usd": usd,
        "eur": eur,
        "rub-usd": rub_usd,
        "rub-eur": rub_eur,
        "usd-eur": usd_eur,
        "sum": {
            "rub": round(total_rub, 2),
            "usd": round(total_usd, 2),
            "eur": round(total_eur, 2)
        }
    }


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