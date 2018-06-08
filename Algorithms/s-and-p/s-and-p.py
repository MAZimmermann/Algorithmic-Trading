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

# Import miscellaneous operating system interfaces module
import os

# Import pandas/pandas_datareader modules
import pandas as pd
import pandas_datareader.data as web

# Import regex module
import re

def save_sp500_tickers():
    
    # Make get request to sklickcharts, store response in resp
    resp = requests.get('https://www.slickcharts.com/sp500')

    # Make new beautiful soup object
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
    
    # Define regex pattern to extract ticker symbol
    regex = "(?<=value=\")(.*)(?=\")"
              
    # Iterate through table (examine each row)
    # "[1:]" allows us to skip row containing column titles
    for row in table.findAll('tr')[1:]:
        tickerTag = str(row.find('input', {'type': 'submit'}))
        ticker = str(re.findall(regex, tickerTag))
        
        # Remove brackets and single quotes
        ticker = ticker.replace("['", "")
        ticker = ticker.replace("']", "")
        
        # Add ticker symbol to 'tickers' list
        tickers.append(ticker)
    
    # Create/open .pickle file ("wb" is write and binary)
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
       
    # Return ticker symbol list
    return tickers

def get_data(reload_sp500=False):
    
    # Use os module to check for file paths
    if os.path.isfile("sp500tickers.pickle"):
        # Open and read sp500tickers.pickle
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    else:
        # Run save_sp500_tickers()
        tickers = save_sp500_tickers()
    
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    
    # Use .now and .timedelta to avoid hardcoding dates
    end = dt.datetime.now()
    start = end - dt.timedelta(days=365)

    for ticker in tickers:
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'iex', start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
            print('Created {}'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)
    
    main_df = pd.DataFrame()
    
    for count,ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('date', inplace=True)
        df.rename(columns = {'close':ticker}, inplace=True)
        df.drop(['open','high','low','volume'],1,inplace=True)
        
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')
        
        if count % 5 == 0:
            print(count)
            
    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')

# Run get data
get_data()
    
compile_data()

# Call save_sp500_tickers() and assign the return to tickerlist
# tickerlist = save_sp500_tickers()

# Sort tickerlist alphabetically
# tickerlist.sort()

# Print the S&P 500 as ticker symbols :)
# print(tickerlist)