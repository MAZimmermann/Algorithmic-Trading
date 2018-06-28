# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 14:21:29 2018

@author: MAZimmermann
"""

# Module for web scraping
import bs4 as bs

# Module for making http requests
import requests

# Change to ticker of your choosing
ticker = 'xom'

url = 'https://www.zacks.com/stock/chart/'+ticker.upper()+'/fundamental/pe-ratio-ttm'

# Make get request to sklickcharts, store response in resp
resp = requests.get(url)

# Make new beautiful soup object
soup = bs.BeautifulSoup(resp.text, "lxml")

# Use bs4 to find 'chart_canvas' tag
chart_canvas = soup.findAll('div', {'id': 'chart_canvas'})

print(chart_canvas)