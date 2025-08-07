# Quant-Tools
A python library containing tools for quantitative finance including: data loading, analysis metrics, simulation and backtesting. This repo is mainly for learning core quant finance principles by implementing them from scratch. 

**Features**
Data Loading: A simple and efficient data loader for historical stock data from yfinance, with local caching to avoid repeated API calls.

Performance Metrics: A suite of functions to calculate key performance and risk metrics, including:
CAGR
Sharpe Ratio
Sortino Ratio
Maximum Drawdown & Drawdown Series
Value at Risk (VaR) & Expected Shortfall (ES)

Simulations: Vectorized functions for financial simulations:
Arithmetic Random Walk
Geometric Brownian Motion (GBM)

Option Pricing:
Monte Carlo pricer for European options.
Finite-difference estimator for Greeks (Delta, Vega, Theta).

Backtesting: A simple, backtesting class for testing different trading strategys.

**Before Usage**
Installation (within powershell)
Clone the repository to your local machine:

git clone https://github.com/YourUsername/quant-tools.git
cd quant-tools

Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate

Install the required packages:
pip install -r requirements.txt
