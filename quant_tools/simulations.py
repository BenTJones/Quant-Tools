import numpy as np
import pandas as pd

def sim_rand_walk(s0,sigma,n_steps,dt = 1):
    #Start with random walk with no drift
    shocks = np.random.randn(n_steps) * sigma * np.sqrt(dt)
    steps = s0 + shocks.cumsum()
    path = np.insert(steps,0,s0)
    return path

def gbm(s0,mu,sigma,n_steps,dt =1):
    #Geometric Brownian Motion simulation
    shocks = np.random.randn(n_steps) * sigma * np.sqrt(dt)
    multipliers = np.exp((mu - 0.5 * sigma**2) * dt + shocks)
    path = np.insert(multipliers,0,s0)
    path = path.cumprod()    
    return path