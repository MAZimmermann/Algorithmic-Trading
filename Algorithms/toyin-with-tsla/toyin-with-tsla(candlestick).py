# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 08:22:16 2018

@author: MAZimmermann

Code replicated/inspired by Sentdex 'Python Programming for Finance'
"""

# Import datetime module
import datetime as dt

# Import pyplot, dates, and style modules
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style

# matplotlib finance module deprecated, using mpl_finance from GitHub
from mpl_finance import candlestick_ohlc

# Import pandas/pandas_datareader
import pandas as pd
import pandas_datareader.data as web

# ggplot style graph
style.use('ggplot')

# Define new datframe, use pandas to read it
df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)

"""
 Resample when you have an overwhelming amount of data, or
  the amount of data you have just isn't necessary
"""

# New dataframe with open, high, low, and close
df_ohlc = df['close'].resample('10D').ohlc()

"""
 Yes, we're starting with open, high, low, and close,
  and tsla never had a stock split (divide shares into two or
   more equal slices)

 BUT, a lot of companies DO have stock splits,
  so you won't be able to use that data

 Must create your own based on the adjusted close
"""

# New dataframe with volume, resample with 10D sum
df_volume = df['volume'].resample('10D').sum()

# Reset the index for df_ohlc
df_ohlc.reset_index(inplace=True)

print(df_ohlc.head())

# Convert datetime object to mdate (matplotlib doesn't use datetime dates...)
df_ohlc['date'] = df_ohlc['date'].map(mdates.date2num)

# Create an axis at specific location inside a regular grid with subplot2grid
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

# Display mdates as dates along x-axis
ax1.xaxis_date()

# candlestick graph on ax1
candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')

# volume on ax2 (fill_between makes it easier to read)
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

plt.show()