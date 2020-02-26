import time
import requests
import pandas as pd
from datetime import datetime


def isotoepochms(t8601="2017-01-02T18:56:01.785Z"):
    t8601 = datetime.strptime(t8601, "%Y-%m-%dT%H:%M:%S.%fZ")
    delta = t8601 - datetime(1970, 1, 1)
    return int(delta.total_seconds()) * 1000 + int(delta.microseconds / 1000)


def orders(
    product="BTC-USD",
    tradeTime="2017-01-02T18:56:01.785Z",
    direction="after",
    limit=100,
):
    if limit > 100:
        limit = 100
        print(
            "Max 100 records per request. To request more records, please use \
              tradeHistory function."
        )

    baseURL = f"https://api.pro.coinbase.com/products/{product}/trades"

    start = 0
    end = requests.get(baseURL).json()[0]["trade_id"]
    mid = requests.get(baseURL + f"?after={int((start + end) / 2) + 1}").json()[0]
    time.sleep(0.67)

    while start < end:
        if mid["time"] == tradeTime:
            break
        if mid["time"] > tradeTime:
            end = mid["trade_id"]
        else:
            start = mid["trade_id"] + 1
        mid = requests.get(baseURL + f"?after={int((start + end) / 2) + 1}").json()[0]
        time.sleep(0.34)

    if "before" == direction:
        return requests.get(baseURL + f"?after={mid['trade_id']}&limit={limit}").json()
    return requests.get(
        baseURL + f"?after={mid['trade_id'] + limit}&limit={limit}"
    ).json()


def tradeHistory(
    product="BTC-USD",
    startTime="2017-01-02T18:56:01.785Z",
    endTime="2017-01-02T19:09:31.97Z",
):
    baseURL = f"https://api.pro.coinbase.com/products/{product}/trades"
    result = orders(product, startTime, direction="after", limit=100)
    time.sleep(0.34)

    IDstamp = result[0]["trade_id"] + 1
    timestamp = result[0]["time"]
    while timestamp < endTime:
        IDstamp += 100
        result = requests.get(baseURL + f"?after={IDstamp}").json() + result
        time.sleep(0.34)
        timestamp = result[0]["time"]

    end = 0
    while result[end]["time"] > endTime:
        end += 1
    return result[end:]


def currencyPrice(product="BTC", tradeTime="2017-01-02T18:56:01.785Z"):
    recent = orders(
        product=f"{product}-USD",
        tradeTime="2017-01-02T18:56:01.785Z",
        direction="after",
        limit=1,
    )[0]
    if recent["time"] == tradeTime:
        return float(recent["price"])
    baseURL = f"https://api.pro.coinbase.com/products/{product}-USD/trades"
    return float(
        requests.get(baseURL + f"?after={recent['trade_id']-1}&limit=1").json()[0][
            "price"
        ]
    )


def rawDataStore(data, filepath="Sample.csv"):
    data = pd.DataFrame(data)[["time", "side", "price", "size", "trade_id"]]
    data["Epoch ms"] = data["time"].map(isotoepochms)
    data.to_csv(filepath, index=False)

