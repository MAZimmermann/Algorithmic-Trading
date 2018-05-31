# -*- coding: utf-8 -*-
"""
Created on Tue May 29 12:04:32 2018

@author: MAZimmermann
"""

"""
This algorithm will not work outside of Quantopian's
 online development environment
"""

# Import Algorithm API functions
from quantopian.algorithm import (
    attach_pipeline,
    pipeline_output,
)

# Pipeline imports
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.psychsignal import stocktwits
from quantopian.pipeline.factors import SimpleMovingAverage
from quantopian.pipeline.filters import QTradableStocksUS


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
    
    # Attach pipeline to algorithm
    attach_pipeline(
        make_pipeline(),
        'data_pipe'
    )

    # Schedule rebalance function
    schedule_function(
        rebalance,
        date_rule=date_rules.week_start(),
        time_rule=time_rules.market_open()
    )


def before_trading_start(context, data):
    # Get pipeline output and
    # store it in context
    context.output = pipeline_output('data_pipe')


def rebalance(context, data):
    # Display first 10 rows
    # of pipeline output
    log.info(context.output.head(10))


# Pipeline definition
def make_pipeline():

    base_universe = QTradableStocksUS()

    sentiment_score = SimpleMovingAverage(
        inputs=[stocktwits.bull_minus_bear],
        window_length=3,
    )

    return Pipeline(
        columns={
            'sentiment_score': sentiment_score,
        },
        screen=(
            base_universe
            & sentiment_score.notnull()
        )
    )