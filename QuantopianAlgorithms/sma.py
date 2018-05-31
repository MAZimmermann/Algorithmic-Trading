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
    
    "initialize" and "handle_data" will be run (called) automatically, no
     need for us to do that ourselves
     
    Delete "handle_data" if you don't plan on using it, or
     remove it's contents ("pass")
    """

    ##########
    
    """
    Define new element in context dictionary
    
    "context" is a python dictionary that stores information on your strategy 
     and passes it to other methods in your algorithm
    
    "sid" allows us to search for companies/equities by name, ticker, etc.
    """
    context.aapl = sid(24)
    
    """
    "schedule_function" allows us to specify how many trades are made in a day
    
    Alternative to "handle_data," which rUnS EVeRY MINuTE!
    """
    schedule_function(ma_crossover_handling,
                      date_rules.every_day(),
                      time_rules.market_open(hours=1))

def ma_crossover_handling(context, data):
    
    """
    "data" is 'universe' of information
    """
    
    ##########
    
    """
    Gather history on aapl
    """
    hist = data.history(context.aapl, 'price', 50, '1d')
    
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
    
def handle_data(context, data):
    
    """
    This method will be called on every trade event for
     the securities you specify, and it rUnS EVeRY MINuTE!
    """
    