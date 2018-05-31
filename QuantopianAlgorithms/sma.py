# -*- coding: utf-8 -*-
"""
Created on Thu May 31 14:36:49 2018

@author: MAZimmermann
"""

"""
This algorithm will not work outside of Quantopian's
 online development environment
"""

def initialize(context):
    
    """
    Initialization logic is placed here
    """
    ##########
    
    """
    The Quantopian environment does a lot "behind the scenes"
        
    "context" is a python dictionary that stores information on your strategy, and
     it is passed to other methods in your algorithm
    
    "initialize" and "handle_data" will be run (called) automatically, no
     need for us to do that ourselves
    """

    ##########
    
    """
    Define new element in context dictionary
    
    "sid" allows us to search for companies/equities by name, ticker, etc.
    """
    context.aapl = sid(24)

def handle_data(context, data):
    
    """
    This method will be called on every trade event for
     the securities you specify
    """

    ##########
    
    """
    "data" is 'universe' of information
    """

    ##########
    
    """
    Gather history on aapl (asset (context.aapl), 
     fields (price), bar_count ("How many fields of this are we interested in..." 50), 
     frequency (one day))
    """
    hist = data.history(context.aapl, 'price', 50, '1d')
    
    """
    Display info in the log provided by Quantopian
    """
    log.info(hist.head())
    
    """
    Caculate a simple moving average for 50 days and 20 days
    """
    sma_50 = hist.mean()
    sma_20 = hist[-20:].mean()
    
    """
    Needed for order bug, must assess open orders before
     creating new order
    """
    open_orders = get_open_orders()
    
    """
    Conditionals to determine when to buy and sell
    
    Quantopian provides a variaty of options for "order_..."
    """
    if sma_20 > sma_50:
        
        if context.aapl not in open_orders:
            """
            Buy! We're targeting 100% (1.0) of our portfolio to be aapl
            """
            order_target_percent(context.aapl, 1.0)
        
    elif sma_20 < sma_50:
        
        if context.aapl not in open_orders:
            """
            Sell! We're targeting 0% (-1.0) of our portfolio to be aapl
            
            Essentially, we're shorting aapl (bet against the company)
            
            Borrow shares from someone at some price, sell at that price,
            buy back at the lower price, and ultimately sell again
            """
            order_target_percent(context.aapl, -1.0)
        
    """
    Needed for debugging
    
    When a large trade is made,
     it takes a while to fill the trade
     
    Since "handle_data" runs every minute,
     new orders are initiated before previous ones close (bad...)
    """    
    record(leverage = context.account.leverage)
    