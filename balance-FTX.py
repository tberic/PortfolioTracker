#!/usr/bin/env python3
from client import FtxClient
import os

api = os.environ.get("ftx_api")
secret = os.environ.get("ftx_secret")
client = FtxClient(api, secret)

response = client._get('wallet/all_balances')

sum = 0.0
for x in response['main']:
	sum += float(x['usdValue'])

now_date = os.environ.get("NOW_DATE")
now_time = os.environ.get("NOW_TIME")

#print('FTX, '+str(now_date)+', '+str(now_time)+', '+str(sum))

import csv
with open('./data/FTX.csv', 'a+', newline='') as csv_file:
        f = csv.writer(csv_file, delimiter = ',')
        f.writerow([str(now_date), str(now_time), "{:.2f}".format(sum)])

