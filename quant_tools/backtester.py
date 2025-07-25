import pandas as pd

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