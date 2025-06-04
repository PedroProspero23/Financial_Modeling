# Multi-Project Financial Evaluation with Excel Input

This project demonstrates how to **evaluate multiple investment projects** using real cash flow data stored in an Excel file. It calculates the **Net Present Value (NPV)**, **Internal Rate of Return (IRR)**, **Payback Period**, and **Return on Investment (ROI)** for each project, generating a final summary report in Excel format.

---

# Objective

Automate the analysis of multiple projects by reading an Excel file with structured cash flow data, and produce a comparative summary of financial viability metrics for each project.

---

# Problem Overview

Each project in the dataset includes:
- A list of annual **cash flows** (positive or negative)
- A specified **discount rate**
- Year-by-year breakdown (from 0 to n)

The script computes:
- **NPV**: Value today of all future cash flows
- **IRR**: Annual rate that makes NPV = 0
- **Payback Period**: First year when cumulative cash flow becomes positive
- **ROI**: Relative return on initial investment

---

# Model Formulation

For each project:
- Cash flows = `[CF_0, CF_1, ..., CF_n]`
- Discount rate = `r`

The calculations include:
- `NPV = Σ(CF_t / (1 + r)^t)`
- `IRR = rate where NPV = 0`
- `Payback = first t where cumulative CF ≥ 0`
- `ROI = (Σ(CF_1 to CF_n) - |CF_0|) / |CF_0|`

---

# Example Input (Excel Format)

| Project | Year | Cash_Flow | Discount_Rate |
|---------|------|-----------|----------------|
| A       | 0    | -100000   | 0.1            |
| A       | 1    | 30000     | 0.1            |
| A       | 2    | 35000     | 0.1            |
| B       | 0    | -120000   | 0.12           |
| B       | 1    | 40000     | 0.12           |
| ...     | ...  | ...       | ...            |

---

# Output

An Excel file named `project_financial_summary.xlsx` will be generated with:

| Project | NPV     | IRR    | Payback_Year | ROI   |
|---------|---------|--------|---------------|--------|
| A       | 17845.20| 0.1412 | 3             | 0.2781 |
| B       | -4231.50| 0.0874 | 4             | 0.1462 |

---


