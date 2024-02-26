import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd

# Fetch historical data for Microsoft
msft_data = yf.download('MSFT', start='2014-01-01', end='2024-01-01')

# Calculate moving averages
msft_data['MA50'] = msft_data['Close'].rolling(window=50).mean()
msft_data['MA200'] = msft_data['Close'].rolling(window=200).mean()

# Prepare the plot
mpf_style = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 8})
addplot = [mpf.make_addplot(msft_data['MA50'], color='blue', width=0.7),
           mpf.make_addplot(msft_data['MA200'], color='red', width=0.7)]

# Find crossover points for annotations
cross_above = (msft_data['MA50'] > msft_data['MA200']) & (msft_data['MA50'].shift(1) < msft_data['MA200'].shift(1))
cross_below = (msft_data['MA50'] < msft_data['MA200']) & (msft_data['MA50'].shift(1) > msft_data['MA200'].shift(1))
msft_data['Cross'] = 0
msft_data.loc[cross_above, 'Cross'] = msft_data['High'] * 1.01
msft_data.loc[cross_below, 'Cross'] = msft_data['Low'] * 0.99
crosses = mpf.make_addplot(msft_data['Cross'], type='scatter', markersize=50, marker='^', color='orange')

# Plotting
mpf.plot(msft_data, type='candle', style=mpf_style, addplot=addplot+[crosses], volume=True, title='Microsoft Stock Price with 50 & 200 Day MAs', ylabel='Price in $')

