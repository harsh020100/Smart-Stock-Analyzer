import yfinance as yf
from yfinance import Ticker


import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt


import seaborn as sns
from io import BytesIO
import base64

import sklearn
from sklearn import linear_model






def company_info(ticker):
    tick=Ticker(ticker)
    return tick.info

def company_history_data(ticker):
    tick=Ticker(ticker)
    return tick.history(period='max')


def plot_closed_data(ticker):
    tick=Ticker(ticker)
    df=tick.history(period='max')
    df['Close'].plot()
    plt.xlabel('Year')
    plt.ylabel('Closing Price')
    #plt.title(f'{ticker} Closing Price History')
    plt.legend()
    # Save the plot as an image in memory
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    plt_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return plt_base64


def plot_daily_return(ticker):
    tick=Ticker(ticker)
    df=tick.history(period='max')
    df['Current_Close']=df['Close'].shift(1)
    df['Daily_Return']=(df['Close']/df['Current_Close'])-1
    df['Daily_Return'].plot()
    plt.xlabel('Year')
    plt.legend()
    # Save the plot as an image in memory
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    plt_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return plt_base64


def plt_daily_return_curve(ticker):
    tick=Ticker(ticker)
    df=tick.history(period='max')
    df['Current_Close']=df['Close'].shift(1)
    df['Daily_Return']=(df['Close']/df['Current_Close'])-1
    sns.displot(data=df,x="Daily_Return",kind='kde')
    plt.xlabel('Daily Return')
    plt.ylabel('Density')
    plt.tight_layout()
     # Save the plot as an image in memory
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    plt_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return plt_base64



#Moving Average
def MA(df,period):
    return df['Close'].rolling(period).mean()


def plot_moving_average(ticker): 
    tick=Ticker(ticker)
    df=tick.history(period='max')
    df['50D-MA'] = MA(df, period=50)
    df['200D-MA'] = MA(df, period=200)
    df['Signal'] = np.where(df['50D-MA'] > df['200D-MA'], df['Close'].max(), -1)


    df['50D-MA'].plot(legend=True)
    df['200D-MA'].plot(legend=True)
    df['Signal'].plot(legend=True)

    plt.title('Low Signal - Indicates (BUY) & High Signal - Indicates (SELL)')

    plt.legend()



     # Save the plot as an image in memory
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    plt_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return plt_base64



def linearRegressionModel(ticker, open_value, high, low, volume):
    tick = Ticker(ticker)
    data = tick.history(period='max')
    reg = linear_model.LinearRegression()
    reg.fit(data[['Open', 'High', 'Low', 'Volume']], data.Close)
    predict = reg.predict([[open_value, high, low, volume]])
    return predict



