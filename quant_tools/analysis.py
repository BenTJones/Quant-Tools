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
 

def calculate_volatility(simple_returns, annualize = True,periods_per_year = 252):
    volatility = simple_returns.std()
    if annualize:
        volatility = volatility * np.sqrt(periods_per_year)
    return volatility

def calculate_sharpe_ratio(simple_returns, risk_free = 0.0,periods_per_year = 252):
    daily_rf = risk_free / periods_per_year
    excess = simple_returns - daily_rf
    mean_excess = excess.mean() * periods_per_year
    std_excess = excess.std() * np.sqrt(periods_per_year)
    sharpe_ratio = mean_excess / std_excess
    return sharpe_ratio

def calculate_drawdown(price_series):
    cummax = price_series.cummax()
    drawdown = (price_series / cummax) - 1 #Calculates % drawdown 
    return drawdown.min()

def anualised_mean(mean_daily,periods_per_year = 252):
    return mean_daily * periods_per_year

def anualised_std(std_daily,periods_per_year = 252):
    return std_daily * np.sqrt(periods_per_year)

def cum_returns(simple_returns):
    return (1 + simple_returns).prod() - 1

def cagr(simple_returns,periods_per_year = 252):
    total = cum_returns(simple_returns)
    n = len(simple_returns)
    years = n / periods_per_year
    cagr = (1+total) ** (1/years) - 1
    return cagr 

def downside_return(simple_returns,mar = 0.0 ,periods_per_year=252):
    