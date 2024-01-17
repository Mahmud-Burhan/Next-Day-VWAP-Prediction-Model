# Next Day VWAP Predictor
# This program predicts the next day VWAP of a stock using Inverse CDF Function and Monte Carlo algorithm
# Stock ticker and number of simulations are adjustable
# The program uses 60 days of historical data (to obtain precise historical VWAP, every 5 minutes trades)
# Developed by: Mahmud bin Burhanudin (github.com/Mahmud-Burhan)
# Date: 2024-01-17
# Version: 1.0.0

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import random as rand
import math
from scipy.stats import norm
from datetime import datetime

# Get stock data
input_stock = str(input("Enter stock ticker: "))

stock = yf.Ticker(input_stock).history(period="60d", interval="5m")
if stock.empty:
    raise Exception("Stock ticker not found")

recent_date = datetime.now().strftime('%Y-%m-%d') + " 00:00:00"
one_day_before_recent_date = (datetime.strptime(recent_date, '%Y-%m-%d %H:%M:%S') - pd.Timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')

stock = stock.loc[:recent_date]
stock = stock.drop(columns=["Open", "Dividends", "Stock Splits"])
stock["Date"] = stock.index
stock["Date"] = stock["Date"].dt.date
stock["Typical Price"] = (stock["High"] + stock["Low"] + stock["Close"])/3
stock["TP x Vol"] = stock["Typical Price"] * stock["Volume"]
stock["Cum(TP x Vol)"] = stock.groupby("Date")["TP x Vol"].cumsum()
stock["Cum(Vol)"] = stock.groupby("Date")["Volume"].cumsum()
stock["VWAP"] = stock["Cum(TP x Vol)"] / stock["Cum(Vol)"]

# Create new dataframe with only single date and VWAP at the end of that day
vwap = stock.drop_duplicates(subset=["Date"], keep="last")
vwap = vwap[["Date", "VWAP"]]
vwap = vwap.reset_index(drop=True)
vwap["Change"] = vwap["VWAP"].diff()
vwap.fillna(0, inplace=True)

# Calculate average change in VWAP
avg_change = vwap["Change"].mean()
# Calculate standard deviation of change in VWAP
std_change = vwap["Change"].std()

# Calculate expected VWAP for next day
# Monte Carlo method
mc_sim = 20000 # Number of simulations ADJUST HERE
simulated_vwap = np.full((2, mc_sim), 0.0)

for i in range(mc_sim):
    simulated_vwap[0, i] = vwap["VWAP"].iloc[-1]
    simulated_vwap[1, i] = vwap["VWAP"].iloc[-1] + norm.ppf(rand.random(), avg_change, std_change)

# Store simulated VWAP end of day values in list and calculate average
simulated_vwap_end = simulated_vwap[1, :].tolist()
simulated_vwap_avg = sum(simulated_vwap_end) / len(simulated_vwap_end)

# Calculate standard deviation of simulated VWAP
simulated_vwap_std = np.std(simulated_vwap_end)
# Calculate probability of VWAP in ranges
mean_plus_std = simulated_vwap_avg + simulated_vwap_std
mean_minus_std = simulated_vwap_avg - simulated_vwap_std
simulated_vwap_for_mean_plus_std = [i for i in simulated_vwap_end if i <= mean_plus_std and i > simulated_vwap_avg]
simulated_vwap_for_mean_minus_std = [i for i in simulated_vwap_end if i >= mean_minus_std and i < simulated_vwap_avg]
simulated_vwap_for_above_mean_plus_std = [i for i in simulated_vwap_end if i > mean_plus_std]
simulated_vwap_for_below_mean_minus_std = [i for i in simulated_vwap_end if i < mean_minus_std]
simulated_vwap_for_mean = [i for i in simulated_vwap_end if i == simulated_vwap_avg]
percentage_for_mean_plus_std = (len(simulated_vwap_for_mean_plus_std) / len(simulated_vwap_end)) * 100
percentage_for_mean_minus_std = (len(simulated_vwap_for_mean_minus_std) / len(simulated_vwap_end)) * 100
percentage_for_above_mean_plus_std = (len(simulated_vwap_for_above_mean_plus_std) / len(simulated_vwap_end)) * 100
percentage_for_below_mean_minus_std = (len(simulated_vwap_for_below_mean_minus_std) / len(simulated_vwap_end)) * 100
percentage_for_mean = (len(simulated_vwap_for_mean) / len(simulated_vwap_end)) * 100

# Plot simulated VWAP using line chart
plt.plot(simulated_vwap)
plt.title(f"Simulated {input_stock} VWAP with {mc_sim} simulations")
plt.xlabel("Next Day")
plt.ylabel("VWAP")
plt.figtext(0.5, -0.05, f"""{datetime.strptime(one_day_before_recent_date, '%Y-%m-%d %H:%M:%S').strftime('%A')} close VWAP is {round(vwap["VWAP"].iloc[-1], 2)}""", ha="center", fontsize=10, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
textbox = '\n'.join([
    f"1 standard deviation is {simulated_vwap_std:.2f}",
    "",
    "Probabilities of tomorrow VWAP in ranges:",
    "",
    f"Above {mean_plus_std:.2f} : {percentage_for_above_mean_plus_std:.2f}%",
    f"{simulated_vwap_avg:.2f} - {mean_plus_std:.2f} : {percentage_for_mean_plus_std:.2f}%",
    "",
    f"Expected (mean) VWAP is {simulated_vwap_avg:.2f}",
    "",
    f"{mean_minus_std:.2f} - {simulated_vwap_avg:.2f} : {percentage_for_mean_minus_std:.2f}%",
    f"below {mean_minus_std:.2f} : {percentage_for_below_mean_minus_std:.2f}%",
    "",
    f"Percentage above mean VWAP: {percentage_for_mean_plus_std + percentage_for_above_mean_plus_std:.2f}%",
    f"Percentage below mean VWAP: {percentage_for_mean_minus_std + percentage_for_below_mean_minus_std:.2f}%"
])
bbox = dict(boxstyle='square', facecolor='lavender', alpha=0.5)
plt.text(1, 0.8, textbox, fontsize=10, bbox=bbox, transform=plt.gcf().transFigure, verticalalignment='top')
plt.show()
