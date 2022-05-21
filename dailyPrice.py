from IPython.display import display, clear_output
from urllib.request import urlopen
import pandas as pd
import datetime
import sched
import time
import json
import dataframe_image as dfi


s = sched.scheduler(time.time, time.sleep)


def tableColor(val):
    if val > 0:
        color = 'red'
    elif val < 0:
        color = 'green'
    else:
        color = 'white'
    return 'color: %s' % color


def stock_crawler(targets):
    clear_output(wait=True)

    # 組成stock_list
    stock_list = '|'.join('tse_{}.tw'.format(target) for target in targets)

    # 　query data
    query_url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=" + stock_list
    data = json.loads(urlopen(query_url).read())

    # 過濾出有用到的欄位
    columns = ['c', 'n', 'z', 'tv', 'v', 'o', 'h', 'l', 'y']
    df = pd.DataFrame(data['msgArray'], columns=columns)
    df.columns = ['股票代號', '公司簡稱', '當盤成交價', '當盤成交量', '累積成交量', '開盤價', '最高價', '最低價', '昨收價']
    df.insert(9, "漲跌百分比", 0.0)

    # 新增漲跌百分比
    for x in range(len(df.index)):
        if df['當盤成交價'].iloc[x] != '-':
            df.iloc[x, [2, 3, 4, 5, 6, 7, 8]] = df.iloc[x, [2, 3, 4, 5, 6, 7, 8]].astype(float)
            df['漲跌百分比'].iloc[x] = (df['當盤成交價'].iloc[x] - df['昨收價'].iloc[x]) / df['昨收價'].iloc[x] * 100

    # 紀錄更新時間
    time = datetime.datetime.now()
    print("更新時間:" + str(time.hour) + ":" + str(time.minute))

    # show table
    df_styled = df.style.applymap(tableColor, subset=['漲跌百分比']).set_precision(2)

    dfi.export(df_styled, "mytable.png",fontsize=16)

    start_time = datetime.datetime.strptime(str(time.date()) + '9:30', '%Y-%m-%d%H:%M')
    end_time = datetime.datetime.strptime(str(time.date()) + '13:30', '%Y-%m-%d%H:%M')

    # 判斷爬蟲終止條件
    if start_time <= time <= end_time:
        s.enter(1, 0, stock_crawler, argument=(targets,))


def daily_report(stock_list):
    s.enter(1, 0, stock_crawler, argument=(stock_list,))
    s.run()
