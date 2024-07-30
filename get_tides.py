import os
import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime,timedelta

# handle proxy
from dotenv import load_dotenv
load_dotenv(override=True)
proxy = os.getenv('PROXY','')
os.environ['HTTP_PROXY'] = proxy
os.environ['http_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['NO_PROXY'] = '127.0.0.1,localhost,.local'
os.environ['no_proxy'] = '127.0.0.1,localhost,.local'

# Victoria Harbour, from January 2020
api_url = "https://api.iwls-sine.azure.cloud-nuage.dfo-mpo.gc.ca/api/v1/stations/5cebf1df3d0f4a073c4bbd1e/data"
dates = pd.date_range('20200101',periods=24*14*25,freq='H')
df = pd.DataFrame(index=dates.tz_localize(tz='UTC'),columns=['wlo','wlp'])

# grab observed and predicted levels
t0 = datetime(2020,1,1)
for wk in range(25):
    t1 = t0 + timedelta(days=14)
    params = {"time-series-code":"wlo",
              "from":t0.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
              "to":t1.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
              "resolution":"SIXTY_MINUTES"}
    r = requests.get(api_url, params=params)
    for x in r.json():
        df.loc[pd.to_datetime(x['eventDate']),'wlo'] = x['value']
    params = {"time-series-code":"wlp",
              "from":t0.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
              "to":t1.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
              "resolution":"SIXTY_MINUTES"}
    r = requests.get(api_url, params=params)
    for x in r.json():
        df.loc[pd.to_datetime(x['eventDate']),'wlp'] = x['value']
    t0 = t1

