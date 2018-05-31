# -*- coding: utf-8 -*-
"""
Created on Thu May 31 14:36:49 2018

@author: MAZimmermann
"""

def initialize(context):
    """
    Initialization logic is placed here, context object passed to
     other methods in your algorithm
    """
    
    context.aapl = sid(24)

def handle_data(context, data):
    """
    This method will be called on every trade event for
     the securities you specify
    """
    
    hist = data.history(context.aapl, 'price', 50, '1d')
    
    log.info(hist.head())
    
    sma_50 = hist.mean()
    
    sma_20 = hist[-20:].mean()