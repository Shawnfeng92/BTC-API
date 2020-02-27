# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 11:13:51 2020

@author: Shawn
"""


import requests
import pandas as pd
import TimeConvert as TC


def tradeHistory(
    product="btcusd",
    startTime="2020-02-23T18:56:01.785Z",
    endTime="2020-02-25T19:09:31.97Z",
):
    baseURL = f"https://api.gemini.com/v1/trades/{product}?timestamp="
    startTime = TC.isotoepochms(startTime) // 1000
    endTime = TC.isotoepochms(endTime) // 1000

    result = requests.get(baseURL + f"{startTime}").json()
    print("Downloading data...")

    timestamp = result[0]["timestamp"]
    while timestamp < endTime:
        result = requests.get(baseURL + f"{timestamp}").json() + result
        timestamp = result[0]["timestamp"] + 1

    end = 0
    while result[end]["timestamp"] > endTime:
        end += 1
    return result[end:]


def rawDataStore(data, filepath="Sample.csv"):
    data = pd.DataFrame(data)
    data["time"] = data["timestampms"].map(TC.epochmstoiso)
    data = data[["time", "type", "price", "amount", "tid", "timestampms"]]
    data.columns = ["Time", "Side", "Price", "Size", "TradeID", "Epoch(ms)"]
    data.to_csv(filepath, index=False)


sample = tradeHistory()
rawDataStore(sample)
