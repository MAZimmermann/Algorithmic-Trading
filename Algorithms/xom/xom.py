# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 14:21:29 2018

@author: MAZimmermann
"""

import pandas as pd
import pandas_datareader.data as web

from datetime import date
start = date(date.today().year, 1, 1)
end = date(date.today().year, 12, 31)

df = web.DataReader('XOM', 'iex', start, end)

print(df.head())