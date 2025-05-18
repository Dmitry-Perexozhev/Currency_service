### Currency service

Currency Service is an asynchronous Python-based application for storing, converting, and analyzing currencies. 

### Key Features:

- Stores and converts currency amounts.
- Calculates total balances in multiple currencies.
- Provides both CLI and API interfaces for interaction.
- Fetches exchange rates asynchronously from external sources.

### Installation requirements

- Python 
- Poetry
- FastAPI
- Uvicorn
- HTTPX
- Requests

### Getting Started
#### Installation 

1) Clone the project repository to your local device:
```
git clone git@github.com:Dmitry-Perexozhev/Currency_service.git
```
2) Go to the project directory:
```
cd Currency_service
```
3) Setting up dependencies with poetry (poetry must be set up early):
```
poetry install
```
4) To use your own currency data parsing source:<br>
    4.1) Specify the source of parsing currency data in service/rates_url.py<br>
    4.2) In file service/provider.py:<br>
        4.2.1) Create a new class from RatesProvider<br>
        4.2.2) Create a method **fetch_rates** according to the parent template

#### Usage

- In the command line, run the application. Example:
```
python3 -m service --rub 1000 --usd 2000 --eur 3000 --period 10 --debug True
```
**--period N**: This is the period in minutes to receive exchange rate data (required)<br>
**--rub 1000**: These are the currency arguments and the initial quantity.<br>
            All currencies that are in the parsing resource are available(at least one value is required)<br>
**--debug True**: Debug mode. Accepts any argument from `0`, `1`, `true`, `false`, `True`, `False`, `y`, `n`, `Y`, `N`. (optional, defaults to false).<br> 
            If the `debug` parameter takes a positive value, output the contents of the web server's `request`/`response` to the console.

- API<br> 
**GET** `/{currency}/get` - Get the amount of funds for **currency**<br> 
**GET** `/amount/get` - The total amount of funds for each of the three currencies, taking into account the current exchange rate, the amount of each currency separately and the current exchange rate<br> 
**POST** `/amount/set` Example Request body:`{"usd": 10}` - Set **usd** 10<br> 
**POST** `/modify` Example Request body:`{"eur": 10, "rub": -20}` - Add 10 to the current amount of **eur**, decrease the current amount of **rub** by 20<br> 

Swagger UI: Interactive API documentation is available at /docs.<br> 

- Feature<br> 
Once per minute, the same data is output to the console as in the response to **GET** `/amount/get`, if the rate of any of the currencies or the amount of funds has changed relative to the previous output to the console.