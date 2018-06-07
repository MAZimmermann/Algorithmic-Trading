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
import re

def save_sp500_tickers():
    
    # make get request to sklickcharts, store response in resp
    resp = requests.get('https://www.slickcharts.com/sp500')

    # make new beautiful soup object
    soup = bs.BeautifulSoup(resp.text, "lxml")
    
    """
     The BeautifulSoup() function takes two arguments
     
     - The string of html to be parsed (resp.text)
     
     
     - The name of the html parser to be used ("lxml")
     
     BeautifulSoup is meant to be used as a wrapper around
      different html parsers
    """
    
    # Use BeautifulSoup to find all table elements of class 'table table-striped table-bordered'
    table = soup.find('table', {'class': 'table table-striped table-bordered'})
    
    # Declare/initialize new empty ticker symbol list
    tickers = []
    
    regex = "(?<=value=\")(.*)(?=\")"
              
    # Iterate through table (examine each row)
    # "[1:]" allows us to skip row containing column titles
    for row in table.findAll('tr')[1:]:
        tickerTag = str(row.find('input', {'type': 'submit'}))
        ticker = str(re.findall(regex, tickerTag))
        ticker = ticker.replace("['", "")
        ticker = ticker.replace("']", "")
        tickers.append(ticker)
    
    # Create/open .pickle file ("wb" is write and binary)
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
       
    # Return ticker symbol list
    return tickers

def get_data(reload_sp500=False):
    
    if os.path.isfile("sp500tickers.pickle"):
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    else:
        tickers = save_sp500_tickers()
    
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