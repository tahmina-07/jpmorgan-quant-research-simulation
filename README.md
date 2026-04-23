# JPMorgan Chase - Quantitative Research Virtual Experience

## What this project does
Estimates the price of natural gas on any given date using cubic spline
interpolation fitted to monthly market data (Oct 2020 — Sep 2024),
with a 1-year extrapolation forward.

## Key result
The model captures the seasonal pattern in gas prices higher in
winter (heating demand) and lower in summer and provides a pricing
function usable for storage contract valuation.

## How to run
pip install pandas numpy matplotlib scipy
python pricer.py

## Usage
from pricer import estimate_price
print(estimate_price("2025-06-15"))  # returns price in $/MMBtu

## Stack
Python · Pandas · NumPy · SciPy · Matplotlib

## Formula 
Value = Revenue from selling
      − Cost of buying
      − Storage cost (rent × months × volume)
      − Injection cost (fee × volume injected)
      − Withdrawal cost (fee × volume withdrawn)

## Source
JPMorgan Chase Quantitative Research Virtual Experience — Forage
