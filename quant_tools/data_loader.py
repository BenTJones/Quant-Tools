import pathlib
from datetime import datetime 
import os

import pandas as pd
import yfinance as yf

cache_directory = '.cache_data' #Cache creation to avoid constantly pulling from API

def get_data(tickers, start='2015-01-01', end=None):
    if end is None:
        end = datetime.today().strftime('%Y-%m-%d')
    
    # Create a single, unique filename for the entire request
    tickers_str = "_".join(sorted(tickers))
    cache_file_name = f'{tickers_str}_{start}_{end}.parquet'
    path = os.path.join(cache_directory, cache_file_name)
    
    if not os.path.exists(cache_directory):
        os.makedirs(cache_directory)
        
    # Check if the cached file exists
    if os.path.exists(path):
        print("Loading data from cache...")
        df = pd.read_parquet(path)
    else:
        print("Downloading data...")
        # Download all tickers at once
        df_raw = yf.download(tickers, start=start, end=end, auto_adjust=False, progress=False)
        
        # Reshape the data by stacking the 'Ticker' level from columns to rows
        df = df_raw.stack()
        
        # Save the clean, reshaped data to the cache
        df.to_parquet(path)
        
    # Ensure the index names are correct
    df.index.names = ['Date', 'Ticker']
    
    return df
