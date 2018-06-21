# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 15:07:06 2018

@author: MAZimmermann
"""

""" import required packages (numpy, pandas, pickle) """
import numpy as np
import pandas as pd
import pickle

def process_data_for_labels(ticker):
    
    # number of days we're looking ahead
    hm_days = 7
    
    # read the pdf we previously saved
    df = pd.read_csv('sp500_joined_closes.csv', index_col=0)
    
    # tolist() might not be necessary?
    tickers = df.columns.values.tolist()
    
    # Replace NA/NaN values with 0
    df.fillna(0, inplace=True)
    
    # Iterate through previous data up to number days specified
    for i in range(1, hm_days + 1):
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]

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
    
    cols = [c for c in args]
    
    # 
    requirements = 0.02
    
    for col in cols:
        
        # Buy
        if col > requirement:
            return 1
        
        # Sell
        if col < -requirement:
            return -1
    
    # Hold
    return 0