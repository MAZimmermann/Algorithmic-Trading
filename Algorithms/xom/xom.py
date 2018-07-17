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
url = 'http://financials.morningstar.com/valuation/price-ratio.html?t='+ticker.upper()

# Make get request to our custom url, store response in resp
resp = requests.get(url)

# Make new beautiful soup object
soup = bs.BeautifulSoup(resp.text, "html.parser")

# This will grab the table element that lists the P/E ratio (and some other values)
table = soup.find('table', {'id': 'currentValuationTable'})

print(soup)

"""for row in table.findAll('tr')[1:]:
    if 'Price/Earnings' not in row.text: 
        continue
    else:
        # We found the P/E :)
        print('Word hey')  """
