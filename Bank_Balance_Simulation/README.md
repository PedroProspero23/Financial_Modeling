# Bank Balance Sheet Analysis & Basel Ratio Visualization

This project simulates a simplified **bank balance sheet** and computes key **prudential financial ratios**, including **liquidity**, **leverage**, and the **Basel index**. A bar chart is also generated to visualize the composition of assets, liabilities, and capital.

---

# Objective

Calculate and visualize a bank's financial structure using realistic balance components and simulate regulatory metrics such as the **Basel Capital Adequacy Ratio**.

---

# Problem Overview

The model includes:
- **Assets**: Loans, Reserves, Investments  
- **Liabilities**: Deposits, Interbank Loans, Short-term Debt  
- **Equity**: Capital  

Each component is associated with a **risk weight** as per Basel standards:
- Loans: 100%  
- Investments: 50%  
- Reserves: 0%  

---

# Financial Indicators Calculated

- **Liquidity Ratio** = Reserves / Deposits  
- **Leverage Ratio** = Total Assets / Capital  
- **Basel Ratio** = Capital / Risk-Weighted Assets  

---

# Example Input

```python
deposits = 8_000_000
loans = 7_000_000
reserves = 2_000_000
capital = 1_000_000
investments = 1_500_000
interbank_loans = 500_000
short_term_debt = 300_000
