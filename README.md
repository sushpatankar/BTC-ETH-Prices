# BTC-ETH-Prices

A web app that is built using Streamlit and Python, which allows tracking the prices of BitCoin and Etherium from two different exchanges Binance and Kraken.

Currently, the web app supports only one currency that is USD however I'm planning to add INR, EUR, and GBP. The chart view is available for both cryptos which use the plotly library of Python.

The app is hosted on Streamlit cloud. Currently, I'm working on hosting it on Heroku.

# Features:

* You can see the current bid (buy) price of the crypto.
* As well as higher bound which is set to 0.02% from the current price of the crypto  
* And lower bound which is 0.012% from the current price of crypto.

```text
Note: Higher and lower bounded prices are the selling price of the crypto. For example, if you buy a BTC at $60,000
the higher bound will be 61,200 i.e. you can sell crypto at 61,200 or any price higher than 61,200. The
lower bound price will be $59,280. The lower bound is set so that you do not suffer heavy loss. 
```

# Tools:
* Python
* Streamlit
* Anaconda
* [Yahoo Finance](https://github.com/ranaroussi/yfinance)
* [CCXT](https://github.com/ccxt/ccxt)
* [fbprophet](https://facebook.github.io/prophet/)
* [Plotly](https://github.com/plotly/plotly.py)

# To run the web app on localhost

* Clone this repository
* Create an anaconda environment

```sh 
conda create --name stock

```
* Once you create the environment run the following commands

```sh 
pip install pystan

```

```sh 
conda install -c conda-forge fbprophet

```

* Install the libraries from requirement.txt
```sh
pip install -r requirements.txt

 ```
 * ***Uncomment the code from lines 11-12 and 213-233 in app.py***
 * Run following command
 ```sh
 streamlit run app.py
 
 ```
## Website:

https://share.streamlit.io/sushpatankar/btc-eth-prices/main/app.py

# Reference:

* [Data Professor Youtube](https://www.youtube.com/channel/UCV8e2g4IWQqK71bbzGDEI4Q)
* [CCTX Tutorial](https://www.youtube.com/watch?v=2Zdm2ISdm1Q)
