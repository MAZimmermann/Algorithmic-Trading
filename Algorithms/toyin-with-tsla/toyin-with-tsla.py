# -*- coding: utf-8 -*-
"""
Created on Thu May 31 17:40:26 2018

@author: MAZimmermann
"""

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

start = dt.datetime(2014,1,1)
end = dt.datetime(2017,12,31)

# Creating new dataframe (basically a spreadsheet)
df = web.DataReader('TSLA', 'iex', start, end)

# "head" prints the first five rows in our dataframe
# print(df.head())

# "tail" prints the last five rows in our dataframe
# print(df.tail())

# Save our dataframe as a csv
df.to_csv('tsla.csv')

# LOTS of different I/O options with pandas
df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)

print(df['close'])

# Dataframe objects have plot attributes
# i.e. pandas will handle matplotlib in the backend for you
df['close'].plot()

plt.show()
