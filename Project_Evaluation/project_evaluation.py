# project_evaluation_simulated.py

import numpy_financial as npf
import numpy as np
import matplotlib.pyplot as plt

# --- Simulated Data ---
initial_investment = 100000.0
years = 5
discount_rate = 0.10  # 10%

# Simulated cash flows (can be changed freely)
cash_flows = [-initial_investment, 20000, 25000, 30000, 30000, 25000]

# --- Evaluation Function ---
def evaluate_project(cash_flows, rate):
    npv = npf.npv(rate, cash_flows)
    irr = npf.irr(cash_flows)
    cumulative = np.cumsum(cash_flows)
    payback = next((i for i, val in enumerate(cumulative) if val >= 0), None)
    return npv, irr, payback, cumulative

# --- Run evaluation ---
npv, irr, payback, cumulative = evaluate_project(cash_flows, discount_rate)

# --- Display Results ---
print("🔹 Simulated Project Evaluation")
print(f"Initial Investment: R$ {initial_investment:,.2f}")
print(f"Discount Rate: {discount_rate*100:.2f}%")
print(f"Cash Flows: {cash_flows}")

print("\n📊 Results:")
print(f"NPV (Net Present Value): R$ {npv:,.2f}")
print(f"IRR (Internal Rate of Return): {irr*100:.2f}%")
print(f"Payback Period: {payback} year(s)" if payback is not None else "Payback Period: Not recovered")

# --- Plot Cumulative Cash Flow ---
plt.figure(figsize=(8, 5))
plt.plot(cumulative, marker='o', color='green', linewidth=2)
plt.axhline(0, color='red', linestyle='--')
plt.title("Cumulative Cash Flow Over Time")
plt.xlabel("Year")
plt.ylabel("Cumulative Cash Flow (R$)")
plt.grid(True)
plt.tight_layout()
plt.show()
