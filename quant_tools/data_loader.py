import pathlib
from datetime import datetime 
import os

import pandas as pd
import yfinance as yf

cache_directory = '.cache_data' #Cache creation to avoid constantly pulling from API

def cache_path(ticker,start,end):
    cache_file_name = f'{ticker}_{start}_{end}.parquet'.replace(':','-')
    return os.path.join(cache_directory,cache_file_name)

def get_data(tickers,start = '2015-01-01',end = None, download = False):
    if end is None:
        end = datetime.today().strftime('%Y-%m-%d')
        
    if isinstance(tickers,str):
        tickers = [tickers] #Converts any single ticker into a list so behaves as desired.
        
    if not os.path.exists(cache_directory):
        os.makedirs(cache_directory)
        
    dataframes = [] #list to store the dataframes for each ticker
    
    for t in tickers:
        path = cache_path(t,start,end) 
        if os.path.exists(path) and not download:
            df = pd.read_parquet(path)
        
        else:
            df = yf.download(t,start = start,end = end,auto_adjust= False, progress=False)
            if df.empty:
                raise ValueError(f'No data available')
            
            df.to_parquet(path)
        df['Ticker'] = t
        dataframes.append(df)
        
    results = pd.concat(dataframes)
    results = results.reset_index().set_index(['Date','Ticker']).sort_index()
    
    return results