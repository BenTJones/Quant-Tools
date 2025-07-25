import numpy as np
import pandas as pd

def calculate_returns(price_series):
    returns = price_series / price_series.shift(1)
    return (returns - 1).dropna()

def calculate_log_returns(price_series):
    returns = np.log(price_series / price_series.shift(1))
    return returns.dropna()
#Calculates day to day returns

def calculate_moving_avg(price_series,window = 20):
    averages_series= price_series.ewm(span = window, adjust = False).mean()
    #Implements Exponential Weighted Average to find trends
    return averages_series
 

def calculate_volatility(returns, annualize = True,periods_per_year = 252):
    volatility = returns.std()
    if annualize:
        volatility = volatility * np.sqrt(periods_per_year)
    return volatility

def calculate_sharpe_ratio(returns, risk_free = 0.0,periods_per_year = 252):
    daily_rf = risk_free / periods_per_year
    excess = returns - daily_rf
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

def cum_returns(returns):
    return (1 + returns).prod() - 1

def cagr(returns,periods_per_year = 252):
    total = cum_returns(returns)
    n = len(returns)
    years = n / periods_per_year
    cagr = (1+total) ** (1/years) - 1
    return cagr 

def downside_deviation(returns,mar = 0.0 ,periods_per_year=252):
    daily_mar = mar / periods_per_year
    negative_excess = returns[returns < daily_mar] - daily_mar
    if negative_excess.empty:
        return 0.0
    downside_deviation_daily = np.sqrt((negative_excess **2).mean())
    return downside_deviation_daily * np.sqrt(periods_per_year)

def sortino_ratio(returns,mar=0.0,periods_per_year=252):
    daily_mar = mar / periods_per_year
    excess = returns - daily_mar
    expected_excess = excess.mean() * periods_per_year
    dd = downside_deviation(returns,mar,periods_per_year)
    sortino = expected_excess / dd
    return sortino if dd != 0 else np.nan

def calmar_ratio(returns,equity_series = None,periods_per_year=252):
    if equity_series is None:
        equity = (1+ returns).cumprod() #Finds equity from £1 investment
    else:
        equity = equity_series
    mdd = calculate_drawdown(equity)
    if mdd == 0:
        return np.nan
    cagr_val = cagr(returns,periods_per_year)
    calmar = cagr_val / abs(mdd)
    return calmar

def drawdown_series(prices):
    peak = prices.cummax()
    drawdowns = (prices / peak) - 1
    return drawdowns

def max_drawdown_duration(prices):
    dds = drawdown_series(prices)
    longest = 0
    current = 0
    for val in dds:
        if val == 0:
            current = 0
        else:
            current += 1
            longest = max(current,longest)
    return longest

from scipy.stats import norm

def VaR_calc(returns,alpha = 0.05 , method = 'historical'):
    if method == 'historical':
        var = returns.quantile(alpha)
        return var
    elif method == 'gaussian':
        mean = returns.mean()
        sd = returns.std()
        z_score = norm.ppf(alpha)
        var = mean + z_score * sd
        return var
    
def expected_shortfall(returns,alpha = 0.05,method = 'historical'):
    var = VaR_calc(returns,alpha,method)
    shortfalls = returns[returns <= var]
    if shortfalls.empty:
        return np.nan
    else:
        mean_shortfall = shortfalls.mean()
        return mean_shortfall