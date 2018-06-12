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

# Import matplotlib, a Python 2D plotting library
import matplotlib.pyplot as plt

# The style package adds support for easy-to-switch plotting "styles"
from matplotlib import style

# ggplot is a plotting system for Python based on R's ggplot2 and the Grammar of Graphics
style.use('ggplot')

# Import numpy, a package for scientific computing in Python
import numpy as np

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

def visualize_data():
    
    """
     Can we find any relationship with the dataset?
    """
    
    # Read sp500_joined_closes.csv into a new dataframe
    df = pd.read_csv('sp500_joined_closes.csv')
    """df['AAPL'].plot()
    plt.show()"""
    
    # Create correlation table of our dataframe
    df_corr = df.corr()
    """
     .corr will look at ALL the information in our dataframe and
      generate correlation values
      
     A new dataframe, df_corr, will be returned
    """
    
    print(df_corr.head())
    
    # Grab the innervalues of df_corr, not index and headers
    data = df_corr.values # NumPy array of collumns and rows
    
    """
     Correlation is a statistical measure of how two securities move in relation
      to eachother
     
     Correlation is represented by the correlation coefficient, which ranges between
      -1 and +1
     
     The prices of two securities move in a similar direction, they are
      often said to be correlated
     
     0 = no correlation
     1 = perfect correlation
     -1 = perfect negative correlation
    """
    
    # Define new figure, outermost plt object housing graphs/plots/etc.
    fig = plt.figure()
    
    # Add subplot, (1,1,1) means our plot will take up the entire figure
    ax = fig.add_subplot(1,1,1)
    
    # We're passing our "data" dataframe and defining our colormap color scheme
    heatmap = ax.pcolor(data, cmap=plt.cm.YlOrBr)
    """
     Heatmaps represent data in the form of a map or diagram in which
      data values are represented as colors
    """
    
    
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
    
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    
    column_labels = df_corr.columns
    row_labels = df_corr.index
    
    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)

    plt.tight_layout()
    
    plt.show
    
# Get the data (don't need to run it again, data already collected)
#get_data()

# Compile the data (don't need to run it again, data already compiled)
#compile_data()

# Visualize the data
visualize_data()

# Call save_sp500_tickers() and assign the return to tickerlist
# tickerlist = save_sp500_tickers()

# Sort tickerlist alphabetically
# tickerlist.sort()

# Print the S&P 500 as ticker symbols :)
# print(tickerlist)