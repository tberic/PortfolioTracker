#!/usr/bin/env python3
import os
import time
import hmac, base64, hashlib
import requests

api_key = os.environ.get("kucoin_api")
api_secret = os.environ.get("kucoin_secret")
api_passphrase = "" # PUT YOUR PASSPHRASE HERE

ask = '/api/v1/accounts'
ask2 = '/api/v1/market/allTickers'

url = 'https://api.kucoin.com' + ask
url2 = 'https://api.kucoin.com' + ask2

now = int(time.time() * 1000)
str_to_sign = str(now) + 'GET' + ask
signature = base64.b64encode(
	hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
passphrase = base64.b64encode(hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
headers = {
"KC-API-SIGN": signature,
"KC-API-TIMESTAMP": str(now),
"KC-API-KEY": api_key,
"KC-API-PASSPHRASE": passphrase,
"KC-API-KEY-VERSION": '2'
}

response = requests.request('get', url, headers=headers)
response2 = requests.request('get', url2, headers=headers)

assets = {}
for x in response.json()['data']:
	if x['currency'] in assets:
		assets[x['currency']] += float(x['balance'])
	else:
		assets[x['currency']] = float(x['balance'])

prices = {}
for x in response2.json()['data']['ticker']:
	prices[x['symbol']] = x['sell']

#print(assets)
sum = 0.0
for token in assets:
	if token == 'USDT':
		sum += float(assets[token])
#		print('USDT: ' + assets[token])
	else:
		if token + '-USDT' in prices:
			val = float(assets[token]) * float(prices[token + '-USDT'])
			sum += val
#			print(token+'-USDT' + str(val))
		elif token+'-BTC' in prices:
			val = (float(assets[token]) * float(prices[token + '-BTC'])) * float(prices['BTC-USDT'])
#			print(token+'BTC' + ' ' + str(val))
			sum += val
		elif token+'-ETH' in prices:
			sum += (float(assets[token]) * float(prices[token + '-ETH'])) * float(prices['ETH-USDT'])

now_date = os.environ.get("NOW_DATE")
now_time = os.environ.get("NOW_TIME")

#print('KUCOIN, '+str(now_date)+', '+str(now_time)+', '+str(sum))

import csv
with open('./data/kucoin.csv', 'a+', newline='') as csv_file:
        f = csv.writer(csv_file, delimiter = ',')
        f.writerow([str(now_date), str(now_time), "{:.2f}".format(sum)])

