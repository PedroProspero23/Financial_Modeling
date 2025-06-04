# Portfolio Optimization using Linear Programming

This project demonstrates how to **optimize a portfolio of assets** using **linear programming**, under budget and risk constraints. The goal is to **maximize expected return** given limited resources.

---

# Objective

Allocate a R$10,000 budget across five assets with known returns, costs, and risk levels, in order to **maximize total expected return** while keeping **total risk within acceptable limits**.

---

# Problem Overview

Each asset has:
- An expected return (e.g., 12%)
- A cost per unit (e.g., R$100)
- A risk contribution per unit (e.g., 0.05)

Constraints:
- Total portfolio cost ≤ R$10,000
- Total risk ≤ 3.5 units

---

# Model Formulation

- **Objective**: Maximize total return  
  → formulated as **minimize negative returns** (since `linprog` minimizes by default)

- **Constraints**:
  - `Σ(cost_i * x_i) ≤ budget`
  - `Σ(risk_i * x_i) ≤ max_risk`
  - `x_i ≥ 0` for all assets

---

# Example Parameters

```python
expected_returns = [0.12, 0.10, 0.14, 0.09, 0.11]
costs_per_unit = [100, 200, 150, 120, 180]
risk_per_unit = [0.05, 0.04, 0.06, 0.03, 0.045]

total_budget = 10000
max_total_risk = 3.5
