import os
import pandas as pd
from pyotp import TOTP
from logzero import logger
from dotenv import load_dotenv
from SmartApi import SmartConnect
import requests
import datetime as dt

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
CLIENT_CODE = os.getenv("CLIENT_ID")
PASSWORD = os.getenv("PIN")
TOTP_SECRET = os.getenv("TOTP_KEY")

smartApi = SmartConnect(api_key=API_KEY)

try:
    totp = TOTP(TOTP_SECRET).now()
except Exception as e:
    logger.error("Invalid Token: The provided token is not valid.")
    raise e

data = smartApi.generateSession(clientCode=CLIENT_CODE, password=PASSWORD, totp=totp)

print(data)

# if data['status'] == False:
#     logger.error(data)


# url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
# response = requests.get(url)
# scrip_data = response.json()

def token_lookup(ticker, scrip_data, exchange="NSE"):
    for scrip in scrip_data:
        if scrip["name"] == ticker and scrip["exch_seg"] == exchange and scrip["symbol"].split("-")[-1] == "EQ":
            return scrip['token']
    return None

def symbol_lookup(token, scrip_data, exchange="NSE"):
    for scrip in scrip_data:
        if scrip["token"] == token and scrip["exch_seg"] == exchange and scrip["symbol"].split("-")[-1] == "EQ":
            return scrip['name']
    return None


def hist_data(ticker, date, interval, scrip_data, exchange="NSE"):
    token = token_lookup(ticker, scrip_data, exchange)
    if token is None:
        logger.error("Invalid Ticker: The provided ticker is not valid.")
        return None
    params = {
        "exchange": exchange,
        "symboltoken": token,
        "interval": interval,
        "fromdate": (dt.date.today() - dt.timedelta(date)).strftime("%Y-%m-%d %H:%M"),
        "todate": dt.date.today().strftime("%Y-%m-%d %H:%M"),
    }
    response = smartApi.getCandleData(params)

    df = pd.DataFrame(response['data'], columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df.set_index('Date', inplace=True)
    df.index = pd.to_datetime(df.index)
    df.index = df.index.tz_localize(None)
    return df

# print(hist_data("RELIANCE", 1, "ONE_MINUTE", scrip_data).head())
