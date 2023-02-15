"""

This document scrapes yahoo finance for stock ticker historical prices

Author: Harshit Shetty 

Date: 14 Feb 2023

"""

#%% Import Pacakges

import numpy as np
import pandas as pd
import requests
import streamlit as st
import datetime 
import plotly.express as px

#%% Web Scrape

ticker = st.sidebar.text_input("Which stock ticker do you want to analyse?", "AAPL")

start_time = st.sidebar.date_input("Pick Start Date:")
end_time =  st.sidebar.date_input("Pick End Date:")

#def stock_data(ticker, start_time, end_time):

start_time = datetime.datetime.combine(start_time, datetime.datetime.min.time())
epoch_start_time = int(start_time.timestamp())

end_time = datetime.datetime.combine(end_time, datetime.datetime.min.time())
epoch_end_time = int(start_time.timestamp())
    
url = "https://query1.finance.yahoo.com/v7/finance/download/" + ticker + "?period1=" + epoch_start_time + "&" + epoch_end_time + "&interval=1d&events=history&includeAdjustedClose=true"

user = {'User-agent':'Mozilla/5.0'}    
site = requests.get(url, headers=user)
df = pd.read_csv(site.text)
filter_df = pd.DataFrame()
df_prices = pd.DataFrame(df.iloc[5])

df_daily_returns = np.log(df_prices).diff()

df_daily_mean = df_daily_returns.mean(axis=0)

daily_returns = df_daily_returns.to_numpy()
exp_ret = df_daily_mean.to_numpy()

fig = px.line(filter_df, x=filter_df.index, y="Adj Close")
st.plotly_chart(fig, use_container_width = True)

    #return df_prices, daily_returns, exp_ret



