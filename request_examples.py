#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 16:34:35 2022

@author: mtuser
"""
import requests

url = 'http://localhost:5001/'
#%% Post(upload) File  

files = {'file': ('trips.csv', open('/home/mtuser/Downloads/trips.csv', 'rb'),'text/csv')}

r = requests.post(url, files=files, verify=False)
print(r.json())
#%% Get the status of all files
url_region = 'http://127.0.0.1:5001/jobs/'
r = requests.get(url_region)
print(r.json())
#%% Get the status of processed files by uuid
url_region = 'http://127.0.0.1:5000/jobs/f24cacbf-d63f-447e-be1b-cfd34e6f39db'
r = requests.get(url_region)
print(r.json())

#%% Get weekly average number of trips for an area, defined by bounding box

url_region = 'http://127.0.0.1:5001/weekly/bbox/6.185303,43.436966,10.085449,45.836454'
r = requests.get(url_region)
print(r.json())

#%% Get weekly average number of trips for an area, defined by Region

url_region = 'http://127.0.0.1:5001/weekly/region/Turin'
r = requests.get(url_region)
print(r.json())