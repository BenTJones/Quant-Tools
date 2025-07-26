import pandas as pd
import numpy as np
from quant_tools.analysis     import (
    calculate_log_returns,
    calculate_sharpe_ratio,
    calculate_drawdown,
    calculate_moving_avg
)



class Portfolio:
    def __init__(self, intial_cash):
        self.cash = intial_cash
        self.stocks = {}
        self.equity_history = []

    def execute(self, orders: dict, price_series):
        for ticker, target in orders.items():
            current = self.stocks.get(ticker, 0.0)
            target = float(target)
            delta = target - current
            cost = price_series[ticker] * delta
            self.cash -= cost
            self.stocks[ticker] = target

    def record_equity(self, date, price_series):
        equity = self.cash
        for ticker, quantity in self.stocks.items():
            equity += price_series[ticker] * quantity
        self.equity_history.append((equity, date))

    def equity_series(self):
        equity_df = pd.DataFrame(
            self.equity_history,
            columns=['equity', 'date']
        )
        equity_series = equity_df.set_index('date')['equity']
        return equity_series


class Backtester:
    def __init__(self, data: pd.DataFrame, strategy, initial_cash):
        self.data = data
        self.strategy = strategy
        self.portfolio = Portfolio(initial_cash)

    def run(self):
        for date, group in self.data.groupby(level='Date'):
            prices = group["Close"].droplevel('Date')
            orders = self.strategy.signal_generation(date, self.data, self.portfolio)
            self.portfolio.execute(orders, prices)
            self.portfolio.record_equity(date, prices)
        return self.portfolio.equity_series()


class MovingAverage:
    # Code for a simple moving average strategy that can be back tested
    def __init__(self, short_win=50, long_win=200):
        self.short_win = short_win
        self.long_win  = long_win

    def short_term_ma(self, price_series: pd.Series):
        sma = calculate_moving_avg(price_series, window=self.short_win)
        last_val = sma.iloc[-1]
        return float(last_val)

    def long_term_ma(self, price_series: pd.Series):
        lma = calculate_moving_avg(price_series, window=self.long_win)
        last_val = lma.iloc[-1]
        return float(last_val)

    def signal_generation(self, date, data, portfolio: Portfolio):
        daily = data.xs(date, level='Date')['Close']
        orders = {}
        for ticker, curr_price in daily.items():
            hist: pd.Series = data.xs(ticker, level=1)['Close'].loc[:date]
            if len(hist) < self.long_win:
                continue
            lma = self.long_term_ma(hist)
            sma = self.short_term_ma(hist)
            pos = portfolio.stocks.get(ticker, 0)
            if lma > sma and pos > 0:
                orders[ticker] = 0
            elif sma > lma and pos == 0:
                target_val = 0.1 * portfolio.cash
                target_shares = target_val / curr_price
                orders[ticker] = target_shares
            else:
                continue
        return orders

