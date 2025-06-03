import matplotlib.pyplot as plt
import pandas as pd

# === 1. INPUT DATA ===

# Main entries (R$)
deposits = 8_000_000
loans = 7_000_000
reserves = 2_000_000
capital = 1_000_000

# Additional balance items
investments = 1_500_000
interbank_loans = 500_000
short_term_debt = 300_000

# Risk weightings (Basel)
rw_loans = 1.0
rw_investments = 0.5
rw_reserves = 0.0

# === 2. BALANCE SHEET CALCULATION ===

# Assets and liabilities
total_assets = loans + reserves + investments
total_liabilities = deposits + interbank_loans + short_term_debt
equity = total_assets - total_liabilities

# Risk-weighted assets
risk_weighted_assets = (loans * rw_loans +
                        investments * rw_investments +
                        reserves * rw_reserves)

# Financial indicators
liquidity_ratio = reserves / deposits
leverage_ratio = total_assets / capital
basel_index = capital / risk_weighted_assets

# === 3. SUMMARY TABLE ===

data = {
    "Item": ["Loans", "Reserves", "Investments", "Deposits",
             "Interbank Loans", "Short-term Debt", "Capital"],
    "Value (R$)": [loans, reserves, investments, deposits,
                   interbank_loans, short_term_debt, capital],
    "Type": ["Asset", "Asset", "Asset", "Liability",
             "Liability", "Liability", "Equity"]
}
df = pd.DataFrame(data)

# === 4. BAR CHART - BALANCE SHEET COMPOSITION ===

colors = {"Asset": "#4CAF50", "Liability": "#F44336", "Equity": "#2196F3"}
df_sorted = df.sort_values(by="Type", ascending=False)

plt.figure(figsize=(10, 6))
plt.bar(df_sorted["Item"], df_sorted["Value (R$)"],
        color=[colors[t] for t in df_sorted["Type"]])
plt.title("📊 Bank Balance Sheet Composition")
plt.ylabel("R$ (millions)")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# === 5. METRICS REPORT ===

print("\n📈 Key Financial Indicators:")
print(f" - Total Assets: R$ {total_assets:,.2f}")
print(f" - Total Liabilities: R$ {total_liabilities:,.2f}")
print(f" - Equity (Net Worth): R$ {equity:,.2f}")
print(f" - Liquidity Ratio (Reserves / Deposits): {liquidity_ratio:.2f}")
print(f" - Leverage Ratio (Assets / Capital): {leverage_ratio:.2f}")
print(f" - Basel Ratio (Capital / RWA): {basel_index:.2%}")
