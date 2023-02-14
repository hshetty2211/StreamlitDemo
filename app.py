import pandas as pd
import streamlit as st

st.write("App Working!")

tickers = ["AAPL", "CSCO", "DIS", "GE", "GS", "IBM", "JNJ", "JPM", "MCD", "MMM", "NKE", "PG"]
ticker = st.selectbox("Pick a ticker", tickers)

df = pd.read_csv(ticker + ".csv", parse_dates=["Date"])

st.write(df)