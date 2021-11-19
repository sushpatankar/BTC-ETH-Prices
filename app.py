import streamlit as st
from datetime import date
import pandas as pd
import yfinance as yf
import ccxt
import os

from random import randint
from streamlit_autorefresh import st_autorefresh

# from fbprophet import Prophet
# from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('ChainAlysis - Stock App')

# Custom function for rounding values
def round_value(input_value):
    if input_value.values > 1:
        a = float(round(input_value, 2))
    else:
        a = float(round(input_value, 8))
    return a

binance = ccxt.binanceus()

kraken = ccxt.kraken()



# print(df)

stocks = ('BTC-USD', 'ETH-USD')
selected_stock = st.selectbox('Select Crypto', stocks)



col1, col2 = st.columns(2)

@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)    
    return data


if selected_stock == 'BTC-USD': 
    binance_ticker = binance.fetch_ticker('BTC/USD')
    binance = binance_ticker['close']
    kraken_ticker = kraken.fetch_ticker('BTC/USD')
    kraken = kraken_ticker['close']
else:
    binance_ticker = binance.fetch_ticker('ETH/USD')
    binance = binance_ticker['close']
    kraken_ticker = kraken.fetch_ticker('ETH/USD')
    kraken = kraken_ticker['close']

data = load_data(selected_stock)

col1.metric(f'{selected_stock} price from Kraken',str((kraken)))
col2.metric(f'{selected_stock} price from Binance', str(binance))

kraken_bid = kraken_ticker['bid']
binance_bid = binance_ticker['bid']

st.header('Buy Prices')
col3, col4 = st.columns(2)


col3.metric(f'{selected_stock} buy price at Kraken',str((kraken_bid)))
col4.metric(f'{selected_stock} buy price at Binance', str(binance_bid))

st.subheader('Suggestion:')
if kraken_ticker['bid'] > binance_ticker['bid']:
    bid = binance_bid
    st.write(f'Buy from Binance. Current buy price at Binance is {binance_bid}. Current Kraken buy price is {kraken_bid}')
else:
    bid = kraken_bid
    st.write(f'Buy from Kareken. Current buy price at Kareken is {kraken_bid}. Current Binance buy price is {binance_bid}.')

st.header("Sell Price")
col5, col6 = st.columns(2)

posSellPrice = bid + bid *0.02
negSellPrice = bid - bid * 0.01

col5.metric(f"For suugested buy price you can sell {selected_stock} after",str(round(posSellPrice,2)))
col6.metric(f"For suugested buy price you can sell {selected_stock} before",str(round(negSellPrice,2)))

left, right = st.columns(2)
with left:
    buy = st.button('Buy Crypto')
with right:
    sell = st.button('Sell Crypto')

if buy:
    if selected_stock == 'BTC-USD':
        if kraken_ticker['bid'] > binance_ticker['bid']:
            with open('btcBuy.txt', "w") as myfile:
                myfile.write(str(binance_bid))
                myfile.write(' from Binance')
            buyPrice = binance_bid
        else:
            with open('btcBuy.txt', "w") as myfile:
                myfile.write(str(kraken_bid))
                myfile.write(' from Kraken')
            buyPrice = kraken_bid
    else:
        if kraken_ticker['bid'] > binance_ticker['bid']:
            with open('ethBuy.txt', "w") as myfile:
                myfile.write(str(binance_bid))
                myfile.write(' from Binance')
            buyPrice = binance_bid
        else:
            with open('ethBuy.txt', "w") as myfile:
                myfile.write(str(kraken_bid))
                myfile.write(' from Kraken')
            buyPrice = kraken_bid


def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0



if selected_stock == 'BTC-USD':
    if is_non_zero_file('btcBuy.txt'):
        st.header('Sell Prices for Crypto you bought:')
        
        with open('btcBuy.txt') as f:
            contents = f.readlines()
            buyCrypto = contents[-1]
            buycrypto = buyCrypto.split(' ')
            sellPrice = float(buycrypto[0])
        
        st.write(f'You bought BTC for ${buyCrypto}!!!')

        posSellPrice = sellPrice+ sellPrice *0.02
        negSellPrice = sellPrice - sellPrice * 0.01
        
        col15,col16 = st.columns(2)
        col15.metric(f'We suggest to sell {selected_stock} that you have bought when it crosses',str(round(posSellPrice,2)))
        col16.metric(f'We suggest to sell  {selected_stock} that you have bought before',str(round(negSellPrice,2)))
        


else:
    if is_non_zero_file('ethBuy.txt'):
        st.header('Sell Prices for Crypto you bought:')
        
        with open('ethBuy.txt') as f:
            contents = f.readlines()
            buyCrypto = contents[-1]
            
            buycrypto = buyCrypto.split(' ')
            sellPrice = float(buycrypto[0])
        posSellPrice = sellPrice+ sellPrice *0.02
        negSellPrice = sellPrice - sellPrice * 0.01

        st.write(f'You bought ETH for ${buyCrypto}!!!')
        col15,col16 = st.columns(2)
        posSellPrice = "{:.2f}".format(posSellPrice)
        negSellPrice = "{:.2f}".format(negSellPrice)

        col15.metric(f'We suggest to sell {selected_stock} when it crosses',str(posSellPrice))
        col16.metric(f'We suggest to sell  {selected_stock} before',str(negSellPrice))
        

    

def plot_raw_data():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
	fig.layout.update(title_text='Time Series data with Rangeslider.', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
	
plot_raw_data()



# Predict forecast with Prophet.
# df_train = data[['Date','Close']]
# df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

# m = Prophet(
# 		changepoint_range=0.8, # percentage of dataset to train on
# 		yearly_seasonality='auto', # taking yearly seasonality into account
# 		weekly_seasonality='auto', # taking weekly seasonality into account
# 		daily_seasonality=False, # taking daily seasonality into account
# 		seasonality_mode='multiplicative' # additive (for more linear data) or multiplicative seasonality (for more non-linear data)
# 	)

# m.fit(df_train)

# ### Predict using the model
# future = m.make_future_dataframe(periods=365)
# forecast = m.predict(future)

    
# st.header(f'Forecast plot for 365 days')
# fig1 = plot_plotly(m, forecast)


# st.plotly_chart(fig1)



st_autorefresh(interval=30000)
