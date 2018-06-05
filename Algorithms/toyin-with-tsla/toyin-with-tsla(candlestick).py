# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 08:22:16 2018

@author: MAZimmermann
"""

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

# Define new datframe, use pandas to read it
df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)

# Open high/low close
df_ohlc = df['close'].resample('10D').ohlc()

# Volume
df_volume = df['volume'].resample('10D').sum()

df_ohlc.reset_index(inplace=True)

#print(df_ohlc.head())

# Convert date to mdates (matplotlib is weird...)
df_ohlc['date'] = df_ohlc['date'].map(mdates.date2num)

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

plt.show()