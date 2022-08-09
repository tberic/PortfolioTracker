#!/usr/bin/env python3
import os
import hashlib
import hmac
import time
import requests
import uuid
import sys
import json


def get(req, headers, payload_string):
	r = requests.post(
	    'https://www.bitstamp.net/api/v2/' + req,
	    headers=headers,
	    data=payload_string
	    )
	c = r.content.decode('UTF-8')
	c = json.loads(c)
	return c


api_key = os.environ.get("bitstamp_api")
API_SECRET = os.environ.get("bitstamp_secret").encode('UTF-8')
client_id = '' # PUT YOUR CLIENT ID HERE

timestamp = str(int(round(time.time() * 1000)))
nonce = str(uuid.uuid4())
content_type = 'application/x-www-form-urlencoded'
payload = {'offset': '1'}

if sys.version_info.major >= 3:
    from urllib.parse import urlencode
else:
    from urllib import urlencode

payload_string = urlencode(payload)

# '' (empty string) in message represents any query parameters or an empty string in case there are none
message = 'BITSTAMP ' + api_key + \
    'POST' + \
    'www.bitstamp.net' + \
    '/api/v2/balance/' + \
    '' + \
    content_type + \
    nonce + \
    timestamp + \
    'v2' + \
    payload_string
message = message.encode('utf-8')
signature = hmac.new(API_SECRET, msg=message, digestmod=hashlib.sha256).hexdigest()
headers = {
    'X-Auth': 'BITSTAMP ' + api_key,
    'X-Auth-Signature': signature,
    'X-Auth-Nonce': nonce,
    'X-Auth-Timestamp': timestamp,
    'X-Auth-Version': 'v2',
    'Content-Type': content_type
}
r = requests.post(
    'https://www.bitstamp.net/api/v2/balance/',
    headers=headers,
    data=payload_string
    )
if not r.status_code == 200:
    raise Exception('Status code not 200')

string_to_sign = (nonce + timestamp + r.headers.get('Content-Type')).encode('utf-8') + r.content
signature_check = hmac.new(API_SECRET, msg=string_to_sign, digestmod=hashlib.sha256).hexdigest()
if not r.headers.get('X-Server-Auth-Signature') == signature_check:
    raise Exception('Signatures do not match')

c = r.content.decode('UTF-8')
c = json.loads(c)

#print(c['usd_balance'])

sum = 0.0
for x in c:
	if 'balance' in x:
		token = x[0:x.find('balance')-1]
		qty = float(c[x])
#		print(token + ' ' + qty)
		if token == 'usd':
			sum += qty
		elif (qty > 0.0001):
			price = get('ticker/'+token+'usd', headers, payload_string)
			sum += qty * float(price['last'])

now_date = os.environ.get("NOW_DATE")
now_time = os.environ.get("NOW_TIME")

#print('BITSTAMP, '+str(now_date)+', '+str(now_time)+', '+str(sum))

import csv
with open('./data/bitstamp.csv', 'a+', newline='') as csv_file:
        f = csv.writer(csv_file, delimiter = ',')
        f.writerow([str(now_date), str(now_time), "{:.2f}".format(sum)])

