from matplotlib import pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc

from pandas_datareader import data as web
import csv
import yfinance as yf
import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd



def show_candelstick(stock_NO):
    yf.pdr_override()

    style.use("ggplot")

    start = (dt.datetime.now() - relativedelta(years=1)).strftime("%Y-%m-%d")
    end = dt.datetime.now().strftime("%Y-%m-%d")

    Analysis = "certain_stock.csv"
    out_csv = csv.writer(open(Analysis, "w"))

    df = web.get_data_yahoo([stock_NO+".TW"], start, end)
    df.to_csv(Analysis)

    data = pd.read_csv(Analysis, parse_dates=True, index_col="Date")

    price = data["Close"]

    moving_avg5 = price.rolling(5).mean()  # 5ma
    moving_avg = price.rolling(20).mean()  # 20ma
    moving_avg50 = price.rolling(50).mean()  # 50ma
    moving_avg80 = price.rolling(80).mean()  # 80ma

    moving_avg_mstd = price.rolling(20).std()

    top = plt.subplot2grid((13, 9), (0, 0), rowspan=9, colspan=9)
    bottom = plt.subplot2grid((13, 9), (11, 0), rowspan=2, colspan=9)
    top.grid(which="both", alpha=0.3)

    # reset date
    data = data.reset_index()
    data["Date"] = data["Date"].apply(lambda d: mdates.date2num(d.to_pydatetime()))
    candlestick = [tuple(x) for x in data[["Date", "Open", "High", "Low", "Close"]].values]
    candlestick_ohlc(top, candlestick, width=0.2, colorup='r', colordown='g', alpha=1)

    top.plot(moving_avg5, color="r", label='MA5', linewidth=1, alpha=0.7)
    top.plot(moving_avg, color="g", label="MA20", linewidth=1, alpha=0.7)
    top.plot(moving_avg50, color="b", label="MA50", linewidth=1, alpha=0.7)

    top.fill_between(moving_avg.index, moving_avg + 2 * moving_avg_mstd, moving_avg - 2 * moving_avg_mstd,
                     color="black",
                     alpha=0.1)
    bottom.bar(data.index, data["Volume"])

    top.legend()
    plt.savefig("candlestickchat.png")
