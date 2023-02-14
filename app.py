import pandas as pd
import streamlit as st

st.write("App Working!")

tickers = ["AAPL", "CSCO", "DIS", "GE", "GS", "IBM", "JNJ", "JPM", "MCD", "MMM", "NKE", "PG"]
ticker = st.selectbox("Pick a ticker", tickers)

df = pd.read_csv(ticker + ".csv", parse_dates=["Date"], index_col=["Date"])

beg_date = df.index.min()
end_date = df.index.max()

pick_start = st.date_input("Pick Start Date:", beg_date)
pick_end = st.date_input("Pick End Date:", end_date)

st.write(df.loc[pick_start:pick_end])