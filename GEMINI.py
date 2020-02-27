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
    startTime="2020-02-20T20:49:52.130Z",
    endTime="2020-02-26T20:49:52.130Z",
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
    data.columns = ["time", "side", "price", "size", "tradeID", "epoch(ms)"]
    
    data.to_csv(filepath, index=False)


sample = tradeHistory()
rawDataStore(sample)
