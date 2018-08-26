import requests
import json
import datetime
import time
import csv
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.animation as animation

export_file = Path("bitcoin_export.csv")

if export_file.is_file():
	pass
else:
	t = csv.writer(open("bitcoin_export.csv", "a"))
	csv_header_window = ("Date", "USD_Price", "Variation", "Diff")
	t.writerow(csv_header_window)

# Input variables
duration_experience = input("Please enter the duration of the experience in minutes (eg 60): ")
duration_experience = int(duration_experience)
duration_experience = duration_experience
bitcoin_frequency = input("Please enter the frequency to update bitcoin value in minutes (eg 1) : ")
bitcoin_frequency = int(bitcoin_frequency)

start_time = time.time()
stop_time = start_time+duration_experience
global actual_time
actual_time = start_time
print(start_time, stop_time)
print("Capture in progress")
while actual_time < stop_time:
	r = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
	bitcoin_data = dict(r.json())
	bitcoin_value = bitcoin_data["bpi"]["USD"]["rate_float"]
	print("Actual Bitcoin pricing ", bitcoin_value, "$")
	if 'last_bitcoin_value' in locals():
		if bitcoin_value > last_bitcoin_value:
			bitcoin_variation = "+"
		elif bitcoin_value < last_bitcoin_value:
			bitcoin_variation = "-"
		else : 
			bitcoin_variation = "="
		bitcoin_diff= bitcoin_value - last_bitcoin_value
		now = datetime.datetime.now()
		t = csv.writer(open("bitcoin_export.csv", "a"))
		export_data = now.strftime("%Y/%m/%d %H:%M"), bitcoin_value, bitcoin_variation, bitcoin_diff
		t.writerow(export_data)
	else:
		now = datetime.datetime.now()
		t = csv.writer(open("bitcoin_export.csv", "a"))
		export_data = now.strftime("%Y/%m/%d %H:%M"), bitcoin_value, None, None
		t.writerow(export_data)
	last_bitcoin_value = bitcoin_value
	actual_time = time.time()
	time.sleep(bitcoin_frequency*60)
print("Capture stopped")
