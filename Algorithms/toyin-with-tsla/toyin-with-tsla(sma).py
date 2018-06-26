# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 17:30:23 2018

@author: MAZimmermann

Code replicated/inspired by Sentdex 'Python Programming for Finance'
"""

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)

df['100ma'] = df['close'].rolling(window=100).mean()

# Can't calculate sma for first 99 data points
# print(df.head())

# drop data frames holding NaN
df.dropna(inplace=True)

# Now we can use head if we want
print(df.tail())

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

# Other parameters inlude line color, label, etc.
ax1.plot(df.index, df['close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['volume'])

plt.show()