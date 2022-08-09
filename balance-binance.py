#!/usr/bin/env python3
import os
from binance.client import Client

def total_amount_usdt(assets, values, token_usdt, prices):
	
	total_amount = 0
	for token in assets:
		if token != 'USDT':
			par = next((item for item in prices if item['symbol'] == token+'USDT'), '-1')
			if (par == '-1'):
				par = next((item for item in prices if item['symbol'] == token+'BUSD'), '-1')
				if (par == '-1'):
					continue
			val = float(values[token]) * float(par['price'])
			total_amount += float(values[token]) * float(par['price'])
#			if (val != 0):
#				print(str(val) + ' ' + token)
		else:
			total_amount += float(values[token]) * 1

	return total_amount


api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')
client = Client(api_key, api_secret)

info = client.get_account()

assets = []
values = {}

for index in range(len(info['balances'])):
	val = 0.0
#	print(info['balances'][index])
	for key in info['balances'][index]:
		if key == 'asset':
			token = info['balances'][index][key]
			assets.append(token)
		if key == 'free':
			val += float(info['balances'][index][key])
		if key == 'locked':
			val += float(info['balances'][index][key])
	values[token] = val

token_usdt = {}
token_pairs = []

for token in assets:
	if token != 'USDT':
		token_pairs.append(token + 'USDT')

prices = client.get_all_tickers()

fut = client.futures_account_balance()
f = 0.0
for x in fut:
	if (x['asset'] == 'USDT'):
		f += float(x['balance'])
	else:
		par = next((item for item in prices if item['symbol'] == token+'USDT'), '-1')
		if par == '-1':
			continue
		f += float(x['balance']) * float(par['price'])

# spot + futures in USDT
sum = float(total_amount_usdt(assets, values, token_usdt, prices))+ float(f)


now_date = os.environ.get("NOW_DATE")
now_time = os.environ.get("NOW_TIME")

#print('BINANCE, '+str(now_date)+', '+str(now_time)+', '+str(sum))

import csv
with open('./data/binance.csv', 'a+', newline='') as csv_file:
	f = csv.writer(csv_file, delimiter = ',')
	f.writerow([str(now_date), str(now_time), "{:.2f}".format(sum)])
