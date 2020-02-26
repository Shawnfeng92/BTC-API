import time
import requests

def orders(product="BTC-USD", tradeTime="2017-01-02T18:56:01.785Z", direction="after", limit=100):
    baseURL = f"https://api.pro.coinbase.com/products/{product}/trades"
    
    start = 0
    end = requests.get(baseURL).json()[0]["trade_id"]
    mid = requests.get(baseURL + f"?after={int((start + end) / 2) + 1}").json()[0]
    time.sleep(0.67)
    
    while start < end:
        if mid["time"] == tradeTime:
            break
        if mid["time"] >= tradeTime:
            end = mid["trade_id"]
        else:
            start = mid["trade_id"] + 1
        mid = requests.get(baseURL + f"?after={int((start + end) / 2) + 1}").json()[0]
        time.sleep(0.34)
    
    if "before" == direction:
        return requests.get(baseURL + f"?after={mid['trade_id']}&limit={limit}").json()
    return requests.get(baseURL + f"?after={mid['trade_id'] + limit}&limit={limit}").json()

def tradeHistory(product="BTC-USD", startTime="2017-01-02T18:56:01.785Z", endTime="2017-01-02T19:09:31.97Z"):
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


