
# from tabulate import tabulate;
# head = ["Ticker","Portfolio weight",
#  "Annualizied volatility","Beta againstS&P500",
# "Beta against Russell 2000","Beta against Dow Jones Industrial average", ];

# print(tabulate(headers=head,tablefmt="grid",tabular_data=));


import pandas as pd
import numpy as np
import yfinance as yf
import scipy.stats as stats
from tabulate import tabulate
from datetime import datetime as dt
import streamlit as st

import pytz


tz = pytz.timezone("America/New_York")
start = tz.localize(dt(2013,1,1))
end = tz.localize(dt.today())



# Set the tickers for the 7 stocks in the portfolio
# tickers = ['AAPL', 'AMZN', 'FB', 'GOOGL', 'JNJ', 'PG', 'V']
tickers = "MA,V,PFE,JPM,BA".split(",")


# Download historical prices for the stocks
prices = df = yf.download(tickers,start, end, auto_adjust=True,ignore_tz=True)['Close']

# yf.download(tickers,start,end,auto_adjust=True ,ignore_tz=True,period='max',)['Adj Close']

# Calculate daily returns
returns = prices.pct_change().dropna()

# Calculate annualized volatility for the past 3 months
volatility = returns.tail(63).std() * np.sqrt(252)

# Calculate betas against SPY, IWM, and DIA for the past 12 months
# benchmarks = ['SPY', 'IWM', 'DIA']
benchmarks="SPY,IWM,DIA".split(",")
betas = pd.DataFrame(columns=benchmarks)
for benchmark in benchmarks:
    benchmark_prices = yf.download(benchmark,start,end ,period='max',auto_adjust=True,ignore_tz=True)['Close']
    benchmark_returns = benchmark_prices.pct_change().dropna()
    # beta = returns.tail(52*5).cov(benchmark_returns.tail(52*5)) / benchmark_returns.tail(52*5).var()
    # betas[benchmark] = beta

# Calculate drawdowns for the past year
week_high = prices.tail(52*5).rolling(window=5).max()
week_low = prices.tail(52*5).rolling(window=5).min()
average_drawdown = ((week_low - week_high) / week_high).mean()
maximum_drawdown = ((week_low - week_high) / week_high).min()

# Calculate total return and annualized total return for the past 10 years
total_return = ((1 + returns.tail(12*10)).cumprod() - 1).tail(1)
annualized_total_return = ((1 + total_return)**(1/10) - 1)

# Create a dataframe to store the risk analysis for each stock
risk_analysis = pd.DataFrame({
    'Ticker': tickers,
    'Portfolio Weight': 1/len(tickers),
    'Annualized Volatility': volatility,
    'Beta vs. SPY': betas['SPY'],
    'Beta vs. IWM': betas['IWM'],
    'Beta vs. DIA': betas['DIA'],
    'Average Weekly Drawdown': average_drawdown,
    'Maximum Weekly Drawdown': maximum_drawdown,
    'Total Return': total_return.values.flatten(),
    'Annualized Total Return': annualized_total_return.values.flatten()
})
risk_analysis.set_index('Ticker', inplace=True)

# Set the tickers for the 3 ETFs
# etf_tickers = ['SPY', 'IWM', 'DIA']
etf_tickers="SPY,IWM,DIA".split(",")

# Calculate the correlation matrix for the portfolio and the 3 ETFs
correlation_matrix = pd.concat([returns, yf.download(etf_tickers,start,end,ignore_tz=True, period='max')['Close'].pct_change().dropna()], axis=1).corr()

# Create a dataframe to store the portfolio risk analysis against the 3 ETFs
portfolio_risk = pd.DataFrame(columns=['ETF Ticker', 'Correlation vs. ETF', 'Covariance vs. ETF', 'Tracking Errors', 'Sharpe Ratio', 'Annualized Volatility Spread'])

# Loop through each ETF and calculate the relevant risk metrics
for etf_ticker in etf_tickers:
    # Calculate the correlation between the portfolio and the ETF
    correlation = correlation_matrix.loc[tickers, etf_ticker].mean()
    
    # Calculate the covariance between the

st.table(prices)
st.table(risk_analysis)
# st.table(correlation)