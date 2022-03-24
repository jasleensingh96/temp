import requests
from datetime import date, timedelta
import json
from tqdm.notebook import tqdm
import pandas as pd

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

url = "https://darksky.net/details/30.7344,76.6594/{0}/si12/en"
#2022-3-1


start_date = date(2021, 10, 1)
end_date = date(2022, 3, 23)
dct = {}
dts = [dt for dt in daterange(start_date, end_date)]
print(len(dts))
for single_date in tqdm(dts):
    dt = single_date.strftime("%Y-%m-%d")
    txt = requests.get(url.format(dt)).text
    txt = txt.split('var hours = ')[-1].split('startHour')[0].strip().rstrip(',')
    dct[dt] = json.loads(txt)

dc = {}
for k, v in dct.items():
    for r in v:
        dc[r['time']] = r

dctt = {}
for i in list(dc.values()):
    kys = ['time', 'summary', 'icon', 'precipIntensity', 'precipProbability', 'temperature', 'apparentTemperature', 'dewPoint', 'humidity', 'pressure', 'windSpeed', 'windGust', 'windBearing', 'cloudCover', 'uvIndex', 'visibility', 'ozone', 'precipType', 'solar']
    for ky in kys:
        dctt[ky] = dctt.get(ky, []) + [i.get(ky, 'NAN')]
pd.DataFrame(dctt).to_csv('temp.csv', index=False)
