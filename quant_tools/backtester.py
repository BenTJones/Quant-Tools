import pandas as pd
import numpy as np

class Portfolio:
    def __init__(self,intial_cash):
        self.cash = intial_cash
        self.stocks = {}
        self.equity_history = []
        
    def execute(self,orders:dict,price_series):
        for ticker,target in orders.items():
            current = self.stocks.get(ticker, 0) #Collects ticker index and if absent replaces with 0
            delta = target - current
            cost = price_series[ticker] * delta
            self.cash -= cost
            self.stocks[ticker] = target
            
    def record_equity(self,date,price_series):
        equity = self.cash
        for ticker,quantity in self.stocks.items():
            equity += price_series[ticker] * quantity
        self.equity_history.append((equity,date))
    
    def equity_series(self):
        equity_df = pd.DataFrame(
            self.equity_history,
            columns = ['equity','date']
        )
        equity_series = equity_df.set_index('date')['equity']
        
        
class Backtester:
    def __init__(self,data:pd.DataFrame,strategy,intial_cash):
        self.data = data
        self.strategy = strategy
        self.portfolio = Portfolio(intial_cash)
        
    def run(self):
        for date, group in self.data.groupby(level = 'date'):
            prices = group['Close']
            orders = self.strategy.signal_generation(date,self.data,self.portfolio)
            self.portfolio.execute(orders,prices)
            self.portfolio.record_equity(date,prices)
        return self.portfolio.equity_series()
    
    
from analysis import calculate_moving_avg    
    
class MovingAverage:
    #Code for a simple moving average strategy that can be back tested
    def __init__(self,short_win = 50, long_win = 200):
         self.short_win = short_win
         self.long_win = long_win

    def short_term_ma(self,prices_series):
        smas = calculate_moving_avg(prices_series,self.short_win)
        sma = smas.iloc[-1]
        return sma
    
    def long_term_ma(self,price_series,):
        lmas = calculate_moving_avg(price_series,self.long_win)
        lma = lmas.iloc[-1]
        return lma
        
    def signal_generation(self,date,data,portfolio:Portfolio):
        prices = data.xs(date,level = 'date')['Close']
        orders = {}
        for ticker, close in prices.items():
            hist = data.xs(ticker,level = 'Ticker')['Close'].loc[:date]
            lma = self.long_term_ma(hist)
            sma = self.short_term_ma(hist)
            current_position = portfolio.stocks[ticker]
            if lma > sma and current_position > 0:
                orders[ticker] = 0
            elif sma > lma and not current_position > 0:
                target_val = 0.1 * portfolio.cash
                target_shares = target_val / close
                orders[ticker] = target_shares
        return orders