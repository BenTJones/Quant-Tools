import numpy as np
import pandas as pd

def calculate_simple_returns(price_series):
    returns = price_series / price_series.shift(1)
    return (returns - 1).dropna()

def calculate_log_returns(price_series):
    returns = np.log(price_series / price_series.shift(1))
    return returns.dropna()
#Calculates day to day returns

def calculate_moving_avg(price_series,window = 20):
    averages_series = price_series.ewm(span = window, adjust = False).mean()
    #Implements Exponential Weighted Average to find trends
    return averages_series

trading_days = 252 

def calculate_volatility(returns, annualize = True):
    volatility = returns.std()
    if annualize:
        volatility = volatility * np.sqrt(trading_days)
    return volatility

def calculate_sharpe_ratio(returns, risk_free = 0.0):
    daily_rf = risk_free / trading_days
    excess = returns - daily_rf
    mean_excess = excess.mean() * trading_days
    std_excess = excess.std() * np.sqrt(trading_days)
    sharpe_ratio = mean_excess / std_excess
    return sharpe_ratio

def calculate_drawdown(price_series):
    cummax = price_series.cummax()
    drawdown = (price_series / cummax) - 1 #Calculates % drawdown 
    return drawdown.min()