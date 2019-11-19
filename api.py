import requests as rq
import json as j
import pandas as pd
import time
import datetime
import csv
import math
import bitfinex

start_data = datetime.date(2016,3,3)
start_unix_time = int(time.mktime(start_data.timetuple()))
start_time = time.strftime("%d\%m\%Y %H:%M", time.localtime(int(start_unix_time)))
qty_candles = 5000
timeFrames = {'m1': 60, 'm5': 60*5, 'm15': 60*15, 'm30': 60*30, 'h1': 60*60, 'h3': 60*180, 'h6': 60*360, 'h12': 60*720, 'D1': 60*720*2, 'D7': 60*720*2*7}
timeFrame = timeFrames['h1']

print(start_unix_time, ': ', start_time)
print('TimeFrame', ': ', timeFrame)


url = 'https://api.bitfinex.com/v2/candles/trade:1h:tBTCUSD/hist?start=1456963200000&sort=+1&limit=5000'
PARAMS = {'start': start_unix_time*1000, 'sort': 1, 'limit': qty_candles}
r = rq.get(url=url)
obj = r.json()
pand = pd.DataFrame(obj)
pand.to_csv ('massive_h1.csv', sep = '\t', header = ['MTS', 'OPEN', 'CLOSE', 'HIGHT', 'LOW', 'VOLUME'], index=False)

with open('massive_h1.csv', 'r') as f1:
    last_line = f1.readlines()[-1]


def add_new_hist():
    with open('massive_h1.csv', 'r') as f1:
        last_line = f1.readlines()[-1]
    last_unix_time = int(last_line[0:14])
    last_time = time.strftime("%d\%m\%Y %H:%M", time.localtime(int(last_unix_time/1000)))
    print(last_time)
    new_params = {'start': last_unix_time, 'sort': +1, 'limit': qty_candles}
    new_hist = rq.get(url=url, params=new_params)
    new_data = new_hist.json()
    new_pand = pd.DataFrame(new_data)
    new_pand.to_csv('massive_h1.csv', sep = '\t',mode = 'a', index = False, header = False)

delta_unix_time = time.time() - start_unix_time
all_candles = delta_unix_time//timeFrame
n = math.ceil(all_candles//qty_candles)

for i in range (int(n)+1):
    add_new_hist()
