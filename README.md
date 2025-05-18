### Currency Service

Currency Service is an asynchronous Python application for storing, converting, and analyzing currencies.

### Key Features

- Stores and converts currency amounts.
- Calculates total balances in multiple currencies.
- Provides both CLI and API interfaces.
- Fetches exchange rates asynchronously from external sources.

### Installation Requirements

- Python 3.12+
- Poetry
- FastAPI
- Uvicorn
- HTTPX
- Requests

### Getting Started

#### Installation

1. Clone the project repository:
```
git clone git@github.com:Dmitry-Perexozhev/Currency_service.git
```
2. Navigate to the project directory:
```
cd Currency_service
```
3. Activate virtual environment:
```
poetry shell
```
3. Install dependencies using Poetry (make sure Poetry is installed):
```
poetry install
```
4. To customize the currency data source:  
- Specify the source URL or method in `service/rates_url.py`.  
- In `service/provider.py`:  
  - Create a subclass of `RatesProvider`.  
  - Implement the `fetch_rates` method according to the base class template.

#### Usage

- Run the application via CLI. Example:
```
python3 -m service --rub 1000 --usd 2000 --eur 3000 --period 10 --debug True
```
- `--period N` — period in minutes for fetching exchange rate data (required).  
- `--rub 1000`, `--usd 2000`, etc. — initial currency amounts. At least one currency amount must be provided.  
- `--debug True` — enables debug mode, printing request and response details to the console. Accepts `0`, `1`, `true`, `false`, `y`, `n` (case-insensitive). Optional, defaults to `false`.

- API Endpoints:  
- **GET** `/{currency}/get` — Get the current amount for the specified currency.  
- **GET** `/amount/get` — Get the total amounts across all currencies, considering current exchange rates.  
- **POST** `/amount/set` with JSON body, e.g., `{"usd": 10}` — Set the amount for a specific currency.  
- **POST** `/modify` with JSON body, e.g., `{"eur": 10, "rub": -20}` — Adjust amounts by adding/subtracting values.

- Swagger UI: Interactive API documentation is available at [`/docs`](http://localhost:8000/docs).

### Additional Features

- The service logs the total currency amounts to the console every minute if there are changes in exchange rates or currency balances, mirroring the output of **GET** `/amount/get`.