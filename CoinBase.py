# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 8:59:02 2020

@author: Shawn
"""


import time
import requests
import pandas as pd
import TimeConvert as TC


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
    print("Searching order...")
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
    startTime="2017-01-01T18:56:01.785Z",
    endTime="2017-01-02T19:09:31.97Z",
):
    baseURL = f"https://api.pro.coinbase.com/products/{product}/trades"
    result = orders(product, startTime, direction="after", limit=100)
    print("Downloading data...")
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
    data["Epoch(ms)"] = data["time"].map(TC.isotoepochms)
    data["time"] = data["Epoch(ms)"].map(TC.epochmstoiso)    
    data.columns = ["time", "side", "price", "size", "tradeID", "epoch(ms)"]

    data.to_csv(filepath, index=False)


sample = tradeHistory()
rawDataStore(sample)
