import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# === 1. SIMULATED ASSET DATA ===

expected_returns = np.array([0.12, 0.10, 0.14, 0.09, 0.11])  # Expected returns (12%, 10%, ...)
costs_per_unit = np.array([100, 200, 150, 120, 180])         # Cost per unit (R$)
risk_per_unit = np.array([0.05, 0.04, 0.06, 0.03, 0.045])    # Relative risk per unit

# === 2. GLOBAL CONSTRAINTS ===

total_budget = 10000       # Total budget (R$)
max_total_risk = 3.5       # Maximum allowed total risk

# === 3. LINEAR PROGRAMMING FORMULATION ===

# Objective: maximize total return → minimize -returns (linprog minimizes by default)
c = -expected_returns

# Constraints:
# 1) total cost ≤ budget
# 2) total risk ≤ max limit
A = [costs_per_unit, risk_per_unit]
b = [total_budget, max_total_risk]

# Variables are non-negative
x_bounds = [(0, None) for _ in range(len(expected_returns))]

# === 4. SOLVING THE LP WITH SIMPLEX ===

res = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method='highs')

if res.success:
    allocation = res.x
    total_return = np.dot(expected_returns, allocation)
    total_cost = np.dot(costs_per_unit, allocation)
    total_risk = np.dot(risk_per_unit, allocation)

    asset_labels = [f"Asset {i+1}" for i in range(len(expected_returns))]

    # === 5. PIE CHART - ALLOCATION ===
    plt.figure(figsize=(10, 5))
    plt.pie(allocation, labels=asset_labels, autopct='%1.1f%%', startangle=140)
    plt.title("Optimal Portfolio Allocation (units per asset)")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

    # === 6. BAR CHART - SUMMARY ===
    plt.figure(figsize=(8, 4))
    plt.bar(['Total Return', 'Total Cost', 'Total Risk'],
            [total_return, total_cost, total_risk],
            color=['green', 'blue', 'red'])
    plt.title("Optimized Portfolio Summary")
    plt.ylabel("Value (R$ or units)")
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

    # === 7. PRINT RESULTS ===
    print("\n📊 Optimization Results:")
    for i, qty in enumerate(allocation):
        print(f" - Asset {i+1}: {qty:.2f} units")
    print(f"\n💰 Expected total return: R$ {total_return:,.2f}")
    print(f"📉 Total portfolio cost: R$ {total_cost:,.2f}")
    print(f"⚠️ Estimated total risk: {total_risk:.2f} units")

else:
    print("❌ Optimization failed:", res.message)
