#!/usr/bin/env python3
import os

sum = 0.0
for filename in os.listdir('/home/pi/crypto/data'):
	if filename.endswith(".csv"):
		with open(os.path.join('/home/pi/crypto/data/', filename), 'r') as f:
			lines = f.readlines()
			last_line = lines[-1].split(',')
			sum += float(last_line[-1])

now_date = os.environ.get("NOW_DATE")
now_time = os.environ.get("NOW_TIME")

import csv
with open('/home/pi/crypto/data/TOTAL.txt', 'a+', newline='') as csv_file:
        f = csv.writer(csv_file, delimiter = ',')
        f.writerow([str(now_date), str(now_time), "{:.2f}".format(sum)])


