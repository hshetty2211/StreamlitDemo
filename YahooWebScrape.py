"""

This document scrapes yahoo finance for stock ticker historical prices

Author: Harshit Shetty 

Date: Feb 2023

"""

#%% Import Pacakges

import pandas as pd
import requests
import streamlit as st
import datetime
import time
import math 
import statsmodels.api as sm
import plotly.express as px

#%% Web Scrape

# Select Ticker & Index
ticker = st.sidebar.text_input("Which stock ticker do you want to analyse?", "GOOG")
st.sidebar.text('Please input stock ticker in ALL CAPS')
index = st.sidebar.text_input("Which index do you want to compare to?", "GSPC")
st.sidebar.text('Please input index ticker in ALL CAPS')

# Select Date Range

# Default Date Ranges
today = datetime.date.today()
one_year = datetime.timedelta(days=366)
start_date = today - one_year # One year ago
one_day = datetime.timedelta(days=1) 
end_date = today - one_day # Yesterday
min_date = datetime.date(2000,1,1)

# Date Inputs
start_time = st.sidebar.date_input("Pick Start Date:", start_date, min_value = min_date, max_value = today)
end_time =  st.sidebar.date_input("Pick End Date:", end_date, min_value = min_date, max_value = today)

# Convert Dates to Unix
start_time = time.mktime(start_time.timetuple())
add_start_time = start_time + 1954.0
start_time = math.trunc(add_start_time)
start_time = str(start_time)

end_time = time.mktime(end_time.timetuple())
add_end_time = end_time + 1954 
end_time = math.trunc(add_end_time)
end_time = str(end_time)

# Build Stock & Index URL and Web Scrape from Yahoo Finance.ca to dataframe
stock_url = "https://query1.finance.yahoo.com/v7/finance/download/" + ticker + "?period1=" + start_time + "&period2=" + end_time + "&interval=1d&events=history&includeAdjustedClose=true"
index_url = "https://query1.finance.yahoo.com/v7/finance/download/%5E" + index + "?period1=" + start_time + "&period2=" + end_time + "&interval=1d&events=history&includeAdjustedClose=true"

user = {'User-agent':'Mozilla/5.0'}    
site_stock = requests.get(stock_url, headers=user)
site_index = requests.get(index_url, headers=user)
stock_data = pd.read_csv(stock_url, parse_dates= ["Date"])
index_data = pd.read_csv(index_url, parse_dates= ["Date"])

# Extract price data for analysis
stock_prices = stock_data[["Date","Adj Close"]]
stock_prices = stock_prices.set_index("Date")

index_prices = index_data[["Date","Adj Close"]]
index_prices = index_prices.set_index("Date")

# Plot price data
fig = px.line(stock_prices, x=stock_prices.index, y="Adj Close")
st.plotly_chart(fig, use_container_width = True)

# Calculate Returns and fit regression model
stock_prices["Returns"] = stock_prices["Adj Close"].pct_change()
index_prices["Returns"] = index_prices["Adj Close"].pct_change()

# Merging Data Sets
merged_data = index_prices.merge(stock_prices, how='inner', left_index=True, right_index=True, suffixes=("_Index","_Stock"))  
merged_data.dropna(inplace=True)

merged_data['Date'] = merged_data.index


# Regression Model
merged_data['Constant'] = 1 #used to calculate alpha or y-intercept 
capm = sm.OLS(merged_data['Returns_Stock'], merged_data[['Returns_Index','Constant']])
results = capm.fit()
summary = results.summary() 

merged_data['Predictions'] = results.predict(merged_data[['Returns_Index','Constant']])
r2 = results.rsquared
beta = results.params[0]

# Regression Visualizations
chartTitle = "Linear Regression {} vs {}".format(ticker, index)
subTitle = "R2:{:.4f} Beta:{:.4f}".format(r2, beta)
fullTitle = "{} <br><sup>{}</sup>".format(chartTitle, subTitle)
xAxisTitle = "{} Returns".format(index)
yAxisTitle = "{} Returns".format(ticker)