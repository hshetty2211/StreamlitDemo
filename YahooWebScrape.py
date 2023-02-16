"""

This document scrapes yahoo finance for stock ticker historical prices

Author: Harshit Shetty 

Date: Feb 2023

"""

#%% Import Pacakges

import numpy as np
import pandas as pd
import requests
import streamlit as st
import datetime
import time
import math 
import plotly.express as px

#%% Web Scrape

# Title
st.title("Stock Analysis")

# Select Ticker
ticker = st.sidebar.text_input("Which stock ticker do you want to analyse?", "GOOG")

# Select Date Range

# Default Date Ranges
today = datetime.date.today()
one_year = datetime.timedelta(days=366)
start_date = today - one_year # One year ago
one_day = datetime.timedelta(days=1) 
end_date = today - one_day # Yesterday

# Date Inputs
start_time = st.sidebar.date_input("Pick Start Date:", start_date)
end_time =  st.sidebar.date_input("Pick End Date:", end_date)

# Convert Dates to Unix
start_time = time.mktime(start_time.timetuple())
add_start_time = start_time + 1954.0
start_time = math.trunc(add_start_time)
start_time = str(start_time)

end_time = time.mktime(end_time.timetuple())
add_end_time = end_time + 1954 
end_time = math.trunc(add_end_time)
end_time = str(end_time)

# Build URL and Web Scrape to dataframe
url = "https://query1.finance.yahoo.com/v7/finance/download/" + ticker + "?period1=" + start_time + "&period2=" + end_time + "&interval=1d&events=history&includeAdjustedClose=true"

user = {'User-agent':'Mozilla/5.0'}    
site = requests.get(url, headers=user)
df = pd.read_csv(url, parse_dates= ["Date"])

# Extract price data for analysis
df_prices = df[["Date","Adj Close"]]
df_prices = df_prices.set_index("Date")

# Plot price data
fig = px.line(df_prices, x=df_prices.index, y="Adj Close")
st.plotly_chart(fig, use_container_width = True)

