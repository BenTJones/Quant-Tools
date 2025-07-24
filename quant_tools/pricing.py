import numpy as np
import pandas as pd
from simulations import gbm

def mc_european_call(s0,K,r,sigma,T,n_steps = 252,n_paths = 10000):
    dt = T/n_steps
    paths_df = gbm(s0,r,sigma,n_steps, dt,n_paths)
    final_prices = paths_df.iloc[-1]
    payoffs = np.maximum(final_prices - K,0)
    expected_payoff = payoffs.mean()
    adjusted_payoff = np.exp(-r*T)* expected_payoff
    return float(adjusted_payoff)

price_estimate = mc_european_call(
    s0=100, K=100, r=0.01, sigma=0.2, T=1.0,
    n_steps=252, n_paths=100_000
)
print(f"Estimated call price: {price_estimate:.4f}")