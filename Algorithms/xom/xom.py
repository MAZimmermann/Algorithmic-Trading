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

# .upper() will change all the letters in 'ticker' to upercase (not sure if this is necessary)
url = 'https://www.marketwatch.com/investing/stock/'+ticker.upper()

# Make get request to our custom url, store response in resp
resp = requests.get(url)

# Make new beautiful soup object
soup = bs.BeautifulSoup(resp.text, "html.parser")

for entry in soup.findAll('small'):
    if 'P/E Ratio' not in entry.text: 
        continue
    else:
        # We found the P/E :)
        print('Word hey')
