# Ensure you have the required packages installed:
# pip install yfinance matplotlib mplfinance

import yfinance as yf
import mplfinance as mpf

# Fetching historical data for Microsoft (MSFT)
msft = yf.Ticker("MSFT")
msft_data = msft.history(period="10y")

# Calculating the 50-day and 200-day moving averages
msft_data['MA50'] = msft_data['Close'].rolling(window=50).mean()
msft_data['MA200'] = msft_data['Close'].rolling(window=200).mean()

# Setting up the moving averages to plot
apd = [mpf.make_addplot(msft_data['MA50'], color='blue', width=0.7),
       mpf.make_addplot(msft_data['MA200'], color='red', width=0.7)]

# Detecting the crossover points
cross_up = (msft_data['MA50'] > msft_data['MA200']) & (msft_data['MA50'].shift() < msft_data['MA200'].shift())
cross_down = (msft_data['MA50'] < msft_data['MA200']) & (msft_data['MA50'].shift() > msft_data['MA200'].shift())

# Adding markers for the crossover points
msft_data['cross_up'] = msft_data.loc[cross_up]['MA50']
msft_data['cross_down'] = msft_data.loc[cross_down]['MA200']

apd += [mpf.make_addplot(msft_data['cross_up'], type='scatter', markersize=100, marker='^', color='green'),
        mpf.make_addplot(msft_data['cross_down'], type='scatter', markersize=100, marker='v', color='black')]

# Plotting the candlestick chart with MA lines and crossover points
mpf.plot(msft_data, type='candle', style='yahoo', addplot=apd, volume=True,
         title="MSFT 10-Year with 50 & 200 DMA", ylabel='Price ($)')

