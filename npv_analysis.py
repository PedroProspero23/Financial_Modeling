# npv_irr_analysis.py

import pandas as pd
import numpy as np
import numpy_financial as npf  # substituto oficial para npv e irr

# Load Excel file
file_path = "C:/Users/pedro/OneDrive/Área de Trabalho/Códigos/3net present value/project_cashflows.xlsx"  # Update if necessary
df = pd.read_excel(file_path)

# Prepare empty result table
projects = df['Project'].unique()
resultados = []

# Calculate metrics for each project
for projeto in projects:
    dados = df[df['Project'] == projeto].sort_values('Year')
    cashflows = dados['Cash_Flow'].values
    rate = dados['Discount_Rate'].iloc[0]

    # NPV
    npv = npf.npv(rate, cashflows)

    # IRR
    try:
        irr = npf.irr(cashflows)
    except:
        irr = None

    # Payback: ano em que o saldo acumulado fica positivo
    cumulative = np.cumsum(cashflows)
    payback = next((i for i, val in enumerate(cumulative) if val >= 0), None)

    # ROI
    total_investment = -cashflows[0]
    total_return = np.sum(cashflows[1:])
    roi = (total_return - total_investment) / total_investment

    resultados.append({
        "Project": projeto,
        "NPV": round(npv, 2),
        "IRR": round(irr, 4) if irr is not None else None,
        "Payback_Year": payback,
        "ROI": round(roi, 4)
    })

# Convert to DataFrame and export
df_result = pd.DataFrame(resultados)
df_result.to_excel("project_financial_summary.xlsx", index=False)
print("✅ Analysis complete. File 'project_financial_summary.xlsx' generated.")
df_result
