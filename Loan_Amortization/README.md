# Loan Amortization Visualization in Python

This project simulates a **fixed-rate loan amortization** schedule and generates a clear visualization of the **remaining balance** and **cumulative interest** over time. It is ideal for illustrating how loan repayments work in monthly installments.

---

# Objective

Calculate and visualize the progression of a loan's balance and interest payments over its full term. Display final values clearly using annotations and generate an educational, professional-quality chart.

---

# Problem Overview

Given:
- A loan amount (`principal`)
- Annual interest rate (`annual_rate`)
- Loan term in years (`years`)

The script calculates:
- Monthly payment (PMT)
- Monthly breakdown of interest and principal
- Cumulative interest paid
- Remaining balance per month

---

# Example Parameters

```python
principal = 50000.0      # Loan amount (R$)
annual_rate = 12.0       # Annual interest (%)
years = 5                # Loan term in years
