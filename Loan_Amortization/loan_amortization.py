# loan_amortization_clean_plot.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Loan parameters ---
principal = 50000.0         # Loan amount (R$)
annual_rate = 12.0          # Annual interest rate (%)
years = 5                   # Loan term in years

monthly_rate = annual_rate / 100 / 12
n_periods = years * 12

# --- Monthly payment calculation (PMT) ---
pmt = principal * monthly_rate / (1 - (1 + monthly_rate) ** -n_periods)

# --- Amortization schedule ---
schedule = []
balance = principal
total_interest = 0

for month in range(1, n_periods + 1):
    interest = balance * monthly_rate
    principal_payment = pmt - interest
    balance -= principal_payment
    total_interest += interest
    schedule.append([
        month,
        round(pmt, 2),
        round(interest, 2),
        round(principal_payment, 2),
        round(balance if balance > 0 else 0, 2),
        round(total_interest, 2)
    ])

df = pd.DataFrame(schedule, columns=["Month", "Payment", "Interest", "Principal", "Balance", "Cumulative Interest"])

# --- Plot with clear annotations ---
fig, ax = plt.subplots(figsize=(10, 6))

# Lines
ax.plot(df["Month"], df["Balance"], label="Remaining Balance", color="blue", linewidth=2)
ax.plot(df["Month"], df["Cumulative Interest"], label="Cumulative Interest", color="orange", linewidth=2)

# Final values for annotation
final_interest = df["Cumulative Interest"].iloc[-1]

# Annotations
ax.annotate("Remaining balance = R$ 0",
            xy=(60, 0), xytext=(45, 5000),
            arrowprops=dict(facecolor='blue', arrowstyle='->'),
            fontsize=10, color='blue')

ax.annotate(f"Total interest paid:\nR$ {final_interest:,.2f}",
            xy=(60, final_interest), xytext=(30, final_interest + 5000),
            arrowprops=dict(facecolor='orange', arrowstyle='->'),
            fontsize=10, color='orange')

# Formatting
ax.set_title("Loan Balance and Interest Over Time", fontsize=14)
ax.set_xlabel("Month")
ax.set_ylabel("Amount (R$)")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()
