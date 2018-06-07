# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 09:52:01 2018

@author: MAZimmermann
"""

# Module for web scraping
import bs4 as bs

# Module for serializing python objects
import pickle

# Module for making http requests
import requests

import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web

def save_sp500_tickers():
    
    # make get request to wikipedia, store response in resp
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

    # make new beautiful soup object
    soup = bs.BeautifulSoup(resp.text, "lxml")
    
    """
     The BeautifulSoup() function takes two arguments
     
     - The string of html to be parsed (resp.text)
     
     
     - The name of the html parser to be used ("lxml")
     
     BeautifulSoup is meant to be used as a wrapper around
      different html parsers
    """
    
    # Use BeautifulSoup to find all table elements of class 'wikitable sortable'
    table = soup.find('table', {'class': 'wikitable sortable'}) 
    
    # Declare/initialize new empty ticker symbol list
    tickers = []
    
    # Iterate through table (examine each row)
    # "[1:]" allows us to skip row containing column titles
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
    
    # Create/open .pickle file ("wb" is write and binary)
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
       
    # Return ticker symbol list
    return tickers

def get_data(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    end = dt.datetime.now()    
    start = end - dt.timedelta(days=365)
    
    for ticker in tickers[:25]:
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'iex', start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
            print('Created {}'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

get_data()

# call save_sp500_tickers() and assign the return to tickerlist
# tickerlist = save_sp500_tickers()

# sort tickerlist alphabetically
# tickerlist.sort()

# Print the S&P 500 as ticker symbols :)
# print(tickerlist)