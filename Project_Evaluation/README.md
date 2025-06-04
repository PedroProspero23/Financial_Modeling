# Project Evaluation with NPV, IRR & Payback Analysis

This project simulates the financial evaluation of an investment project using standard capital budgeting techniques: **Net Present Value (NPV)**, **Internal Rate of Return (IRR)**, and **Payback Period**.

---

# Objective

Assess the viability of a simulated investment over a 5-year period based on forecasted cash flows and a given discount rate.

---

# Methodology

- Use of a **discount rate** (10%) to discount future cash flows
- Calculation of:
  - **NPV**: Net Present Value
  - **IRR**: Internal Rate of Return
  - **Payback**: Number of periods to recover the initial investment
- Visualization of **cumulative cash flows** over time

---

# Example Scenario

```python
initial_investment = 100000.0
cash_flows = [-initial_investment, 20000, 25000, 30000, 30000, 25000]
discount_rate = 0.10
