# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 15:07:06 2018

@author: MAZimmermann

Code replicated/inspired by Sentdex 'Python Programming for Finance'
"""

# Import Counter
from collections import Counter

# Import numpy, pandas, and pickle
import numpy as np
import pandas as pd
import pickle

# Import modules/classifiers from sklearn
from sklearn import svm, cross_validation, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

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
    requirement = 0.05
    
    # Iterate through cols
    for col in cols:
        if col > requirement: # Buy!
            return 1
        if col < -requirement: # Sell!
            return -1
    
    # Hold (neither of the conditions above were met, return 0)
    return 0

def extract_featuresets(ticker):
    
    # Call process_data_for_labels and pass the desired ticker as the paramter
    tickers, df = process_data_for_labels(ticker)
    
    # Generates new collumn with buy, sell, or hold
    df['{}_target'.format(ticker)] = list(map(buy_sell_hold,
                                               df['{}_1d'.format(ticker)],
                                               df['{}_2d'.format(ticker)],
                                               df['{}_3d'.format(ticker)],
                                               df['{}_4d'.format(ticker)],
                                               df['{}_5d'.format(ticker)],
                                               df['{}_6d'.format(ticker)],
                                               df['{}_7d'.format(ticker)]))
    
    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data spread:', Counter(str_vals))
    
    df.fillna(0, inplace=True)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)
    
    df_vals = df[[ticker for ticker in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)
    
    # 'X' feature sets, 'y' labels
    X = df_vals.values
    y = df['{}_target'.format(ticker)].values
    
    return X, y, df

def learn(ticker):
    
    # extract_featuresets('__') will return X, y, and df
    X, y, df = extract_featuresets('XOM')
    
    # Define training and testing
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size = 0.25)
    
    # Voting classifier that combines three distinct classifiers
    clf = VotingClassifier([('lsvc', svm.LinearSVC()),
                            ('knn', neighbors.KNeighborsClassifier()),
                            ('rfor', RandomForestClassifier())])
 
    
    # X is the percent change data for all of the companies, and y is the target (0, 1, or -1)
    clf.fit(X_train, y_train) # We need to "fit" the input data to the target
    
    confidence = clf.score(X_test, y_test)
    print('Accuracy:', confidence)
    
    predictions = clf.predict(X_test)
    print('Predicted spread:', Counter(predictions))
    
    """
     In the future... if you train and are happy with the confidence value,
      just run clf.predict
     
     If you don't want to retrain this model again, pickle out the classifier,
      load in the classifier, and run clf.predict
    """
    
    return confidence

learn('BAC')
    
    
    