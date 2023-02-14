import pandas as pd
import streamlit as st

st.write("App Working!")

tickers = ["AAPL", "MSFT", "NFLX"]
st.selectbox("Pick a ticker", tickers)