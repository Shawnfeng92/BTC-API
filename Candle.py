# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 14:22:30 2020

@author: Shawn
"""


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpl_finance as mpf


def candlegraph(filepath="Sample.csv", title="Sample"):
    # Draw candlestick chart based on given trade history.
    # Every candle contains real body, upper shadow and lower shadow.
    # Here, I use red color as down trend and green color as up trend.
    # The top of the red real body is the open price, the bottom of the red
    # real body is the close price. The top of the green real body is the close
    # price, the bottom of the green real body is the open price.
    # The top of the upper shadow is the high price and the bottom of the lower
    # shadow is the low price.

    # reading data from csv file
    df = pd.read_csv(filepath, parse_dates=True, index_col=0)

    # create ohlc, volume, vwap and notional value df
    df_ohlc = df["price"].resample("1h").ohlc()
    df_ohlc.reset_index(inplace=True)
    df_ohlc["Time"] = df_ohlc["time"].map(mdates.date2num)

    df_volume = df["size"].resample("1h").sum()

    df_vwap = []
    df_nv = []

    starttime = df["Epoch(ms)"][-1] // 3600000 * 3600000
    endtime = df["Epoch(ms)"][0] // 3600000 * 3600000 + 3600001

    time_point = range(starttime, endtime, 3600000)
    for i in range(len(time_point) - 1):
        temp = df.loc[
            (df["Epoch(ms)"] >= time_point[i]) & (df["Epoch(ms)"] < time_point[i + 1])
        ]
        df_vwap.append(sum(temp["price"] * temp["size"]) / sum(temp["size"]))
        df_nv.append(sum(temp["price"] * temp["size"]))

    # create canvas fig and two subplots ax and ax2
    fig = plt.figure(figsize=(17, 10))

    ax = fig.add_axes([0, 0.4, 1, 0.6])
    ax2 = fig.add_axes([0, 0.2, 1, 0.2])
    ax3 = fig.add_axes([0, 0, 1, 0.2])

    # set tile, xtick, ylabel for ax
    ax.set_title(title)
    xtick = []
    for i in df_ohlc["time"]:
        xtick.append(i.ctime()[11:13])
    ax.set_xticklabels(xtick)
    ax.set_ylabel("Trade Price")

    # draw ohlc bar chart
    mpf.candlestick2_ochl(
        ax,
        df_ohlc["open"],
        df_ohlc["close"],
        df_ohlc["high"],
        df_ohlc["low"],
        width=0.5,
        colorup="g",
        colordown="r",
        alpha=0.6,
    )

    # add vwap line chart
    ax.plot(df_vwap, "bo-", label="Volume Weighted Average Price")
    ax.legend(loc="upper right")
    ax.grid(True)

    # set xtick, ylabel for ax2
    ax2.set_xticks(range(0, len(df_ohlc["Time"]), 1))
    ax2.set_xticklabels(xtick)
    ax2.set_ylabel("Trade Volume")

    # draw volume bar chart
    mpf.volume_overlay(
        ax2,
        df_ohlc["open"],
        df_ohlc["close"],
        df_volume,
        colorup="g",
        colordown="r",
        width=0.5,
        alpha=0.8,
    )
    ax2.grid(True)

    # set xtick, ylabel for ax3
    ax3.set_xticks(range(0, len(df_ohlc["Time"]), 1))
    ax3.set_xticklabels(xtick)
    ax3.set_ylabel("Notional Value")

    # draw volume bar chart
    mpf.volume_overlay(
        ax3,
        df_ohlc["open"],
        df_ohlc["close"],
        df_nv,
        colorup="g",
        colordown="r",
        width=0.5,
        alpha=0.8,
    )
    ax3.grid(True)

    # create shared xlabel
    plt.xlabel("Time")

    # put together
    plt.subplots_adjust(hspace=0)


candlegraph()
