# JPMorgan Chase — Quantitative Research Virtual Experience
# Task 1: Natural Gas Price Estimation
# Builds a price curve from monthly data and estimates price on any date

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from datetime import datetime

# ── 1. LOAD DATA 
df = pd.read_csv("Nat_Gas.csv")
df["Dates"]  = pd.to_datetime(df["Dates"], format="%m/%d/%y")
df = df.sort_values("Dates").reset_index(drop=True)
df["days"]   = (df["Dates"] - df["Dates"].min()).dt.days
start_date = df["Dates"].min()
print("Data loaded:", df.shape)

# ── 2. VISUALIZE ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 4))

axes[0].plot(df["Dates"], df["Prices"], "o-", color="steelblue",
             linewidth=1.5, markersize=4)
axes[0].set_title("Gas Prices Over Time")
axes[0].set_xlabel("Date")
axes[0].set_ylabel("Price ($/MMBtu)")
axes[0].grid(True, alpha=0.3)

df["month"] = df["Dates"].dt.month
monthly   = df.groupby("month")["Prices"].mean()
axes[1].bar(range(1,13), monthly, color="coral", edgecolor="white")
axes[1].set_title("Average Price by Month (Seasonal Pattern)")
axes[1].set_xlabel("Month")
axes[1].set_xticks(range(1,13))
axes[1].set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun",
                              "Jul","Aug","Sep","Oct","Nov","Dec"])
axes[1].grid(True, alpha=0.3, axis="y")

plt.tight_layout()
plt.savefig("seasonal_analysis.png", dpi=120)
plt.show()

# ── 3. FIT CUBIC SPLINE ───────────────────────────────────────────────────────
spline = CubicSpline(df["days"], df["Prices"])

# ── 4. EXTRAPOLATE 1 YEAR FORWARD ─────────────────────────────────────────────
last_day  = int(df["days"].max())
all_days  = np.linspace(0, last_day + 365, 1000)
all_dates = [start_date + pd.Timedelta(days=int(d)) for d in all_days]

plt.figure(figsize=(13, 5))
plt.plot(df["Dates"], df["Prices"], "o",
         color="steelblue", markersize=5, label="Known data")
plt.plot(all_dates, spline(all_days),
         color="steelblue", linewidth=1.2, alpha=0.6, label="Spline curve")
plt.axvline(df["Dates"].max(), color="red",
             linestyle="--", linewidth=1, label="Extrapolation starts")
plt.title("Price Curve — Historical + 1-Year Forecast")
plt.xlabel("Date")
plt.ylabel("Price ($/MMBtu)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("price_curve.png", dpi=120)
plt.show()

# ── 5. PRICING FUNCTION ───────────────────────────────────────────────────────
def estimate_price(date_str: str) -> float:
    """Return estimated gas price for any date (format: YYYY-MM-DD)."""
    target = datetime.strptime(date_str, "%Y-%m-%d")
    days   = (target - start_date.to_pydatetime()).days
    return round(float(spline(days)), 4)

# ── 6. TEST IT ────────────────────────────────────────────────────────────────
print("\n── Price Estimates ──────────────────────────")
for d in ["2021-06-15", "2022-01-31", "2024-09-30", "2025-03-15", "2025-09-30"]:
    print(f"  {d}  →  ${estimate_price(d):.2f} / MMBtu")
