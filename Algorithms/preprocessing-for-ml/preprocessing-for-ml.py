# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 15:07:06 2018

@author: MAZimmermann

Code replicated/inspired by Sentdex 'Python Programming for Finance'
"""

""" import required packages (numpy, pandas, pickle) """
import numpy as np
import pandas as pd
import pickle

from collections import counter

def process_data_for_labels(ticker):
    
    # How many days do we have in the future to make or lose __%
    hm_days = 7
    
    # read the pdf we previously created/saved
    df = pd.read_csv('sp500_joined_closes.csv', index_col=0)
    
    # tolist() might not be necessary?
    tickers = df.columns.values.tolist()
    
    # Replace NA/NaN values with 0
    df.fillna(0, inplace=True)
    
    # Iterate through previous data up to number days specified
    for i in range(1, hm_days + 1):
        # On day __ into the future, what is the value in percent change?
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]
        # Price __ days from now minus today's price, divided by today's price

    # Replace NA/NaN values with 0
    df.fillna(0, inplace=True)
    return tickers, df

def buy_sell_hold(*args):

    """
     This function will produce buy, sell, and hold values that
      will be mapped to a new column in our dataframe
    
     1 indicates buy
     
     -1 indicates sell
     
     0 indicates hold
    """
    
    # Iterate by row, but pass columns as parameters
    cols = [c for c in args]
    
    # Set stock price change requirement (in this case, 2%)
    requirement = 0.02
    
    # Iterate through cols
    for col in cols:
        if col > requirement: # Buy!
            return 1
        if col < -requirement: # Sell!
            return -1
    
    # Hold (neither of the conditions above were met, return 0)
    return 0

def extract_featuresets(ticker):
    tickers, df = process_data_for_labels(ticker)
    df['{}_target'.format(ticker)] = list(map(buy_sell_hold, 
       df['{}_1d'.format(ticker, i)],
       df['{}_2d'.format(ticker, i)],
       df['{}_3d'.format(ticker, i)],
       df['{}_4d'.format(ticker, i)],
       df['{}_5d'.format(ticker, i)],
       df['{}_6d'.format(ticker, i)],
       df['{}_7d'.format(ticker, i)]
       ))
    vals = df['{}_target'.format(ticker, i)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data spread:', Counter(str_vals))
    
    df.fillna(0, inplace=True)
    df = df.replace([np.inf, -np.inf, np.nan])
    df.dropna(inplace=True)
    
    df_vals = df[[ticker for ticker in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf, 0])
    df_vals.fillna(0, inplace=True)
    
    # 'X' feature sets, 'y' labels
    X = df_vals.values
    y = df['{}_target'.format(ticker)].values
    
    return X, y, df
    
