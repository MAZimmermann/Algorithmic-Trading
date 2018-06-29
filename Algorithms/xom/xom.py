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
url = 'https://www.zacks.com/stock/chart/'+ticker.upper()+'/fundamental/pe-ratio-ttm'

# Make get request to our custom url, store response in resp
resp = requests.get(url)

# Make new beautiful soup object
soup = bs.BeautifulSoup(resp.text, "lxml")

# This will grab descriptive section containing the current P/E
section = soup.find('section', {'id': 'stock_comp_desc'})

# zacks.com has a predictable format for listing a companies P/E
start = 'trailing-twelve-months P/E of'
end = 'compared to'

for ptag in section.findAll('p'):
    if "trailing-twelve-months P/E of" not in ptag.text: 
        continue
    else:
        # We found the P/E :)
        theGoods = ptag.text[ptag.text.find(start):ptag.text.find(end)]
        print(ticker,"has a",theGoods)