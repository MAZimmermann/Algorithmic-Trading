# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 17:30:23 2018

@author: MAZimmermann
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