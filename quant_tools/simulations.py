import numpy as np
import pandas as pd

def sim_rand_walk(s0,sigma,n_steps,dt = 1/252):
    #Start with random walk with no drift
    shocks = np.random.randn(n_steps) * sigma * np.sqrt(dt)
    steps = s0 + shocks.cumsum()
    path = np.insert(steps,0,s0)
    return path

def gbm(s0,mu,sigma,n_steps,dt =1/252,n_paths = 1):
    #Geometric Brownian Motion simulation
    shocks = np.random.randn(n_steps,n_paths) * sigma * np.sqrt(dt)
    multipliers = np.exp((mu - 0.5 * sigma**2) * dt + shocks)
    initial_prices = s0 * np.ones(n_paths)
    paths = np.vstack([initial_prices,multipliers])
    paths = paths.cumprod(axis = 0)
    paths_df = pd.DataFrame(
        paths,
        index = [pd.RangeIndex(0,n_steps+1,name='step')],
        columns= [f'path_{i}' for i in range(n_paths)]
    )    
    return paths_df

    