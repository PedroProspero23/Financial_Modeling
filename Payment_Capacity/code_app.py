# app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile
import io

st.set_page_config(page_title="Payment Capacity Analysis - Agribusiness Sector", layout="wide")
st.title("🏦 Corporate Payment Capacity Analysis")

tabs = st.tabs(["📋 Manual Input", "📁 Import CSV Batch"])

# Helper functions
def safe_div(n, d):
    return round(n / d, 2) if d else None

def normalize(v, mi, ma):
    return max(0, min((v - mi) / (ma - mi), 1)) if v is not None else 0

def calculate_indicators(row):
    indicators = {}
    indicators["Current Liquidity"] = safe_div(row["ativo_circulante"], row["passivo_circulante"])
    indicators["Quick Ratio"] = safe_div(row["ativo_circulante"] - row["estoques"], row["passivo_circulante"])
    indicators["Immediate Liquidity"] = safe_div(row["disponivel"], row["passivo_circulante"])
    indicators["Total Debt Ratio"] = safe_div(row["passivo_total"], row["ativo_total"])
    indicators["ROE"] = safe_div(row["lucro_liquido"], row["patrimonio_liquido"])
    indicators["DSCR"] = safe_div(row["fluxo_caixa_operacional"], row["servico_divida"])
    indicators["Interest Coverage"] = safe_div(row["ebitda"], row["servico_divida"])
    return indicators

def classify_rating(ind):
    score = 0
    if ind["Current Liquidity"] is not None:
        score += 3 if ind["Current Liquidity"] >= 1.5 else 2 if ind["Current Liquidity"] >= 1 else 1
    if ind["Total Debt Ratio"] is not None:
        score += 3 if ind["Total Debt Ratio"] <= 0.5 else 2 if ind["Total Debt Ratio"] <= 0.7 else 1
    if ind["DSCR"] is not None:
        score += 6 if ind["DSCR"] >= 2 else 4 if ind["DSCR"] >= 1.2 else 2
    if ind["ROE"] is not None:
        score += 3 if ind["ROE"] >= 0.15 else 2 if ind["ROE"] >= 0.05 else 1

    if score >= 14:
        return "A", 0.90
    elif score >= 10:
        return "B", 0.75
    elif score >= 7:
        return "C", 0.50
    else:
        return "D", 0.00

# Variable to store the PDF
pdf_bytes = None

with tabs[0]:
    st.sidebar.header("📋 Company Financial Data")
    receita_total = st.sidebar.number_input("Net annual revenue (R$)", 0.0, step=1000.0)
    lucro_liquido = st.sidebar.number_input("Net income (R$)", 0.0, step=1000.0)
    ativo_circulante = st.sidebar.number_input("Current assets (R$)", 0.0, step=1000.0)
    passivo_circulante = st.sidebar.number_input("Current liabilities (R$)", 0.0, step=1000.0)
    estoques = st.sidebar.number_input("Inventory (R$)", 0.0, step=1000.0)
    disponivel = st.sidebar.number_input("Cash and equivalents (R$)", 0.0, step=1000.0)
    ativo_total = st.sidebar.number_input("Total assets (R$)", 0.0, step=1000.0)
    passivo_total = st.sidebar.number_input("Total liabilities (R$)", 0.0, step=1000.0)
    patrimonio_liquido = st.sidebar.number_input("Shareholders' equity (R$)", 0.0, step=1000.0)
    servico_divida = st.sidebar.number_input("Annual debt service (R$)", 0.0, step=1000.0)
    ebitda = st.sidebar.number_input("Annual EBITDA (R$)", 0.0, step=1000.0)
    fluxo_caixa_operacional = st.sidebar.number_input("Operating cash flow (R$)", 0.0, step=1000.0)
    valor_garantia = st.sidebar.number_input("Collateral value (R$)", 0.0, step=1000.0)
    tipo_garantia = st.sidebar.selectbox("Collateral type", ["Real Estate", "Equipment", "Vehicle", "Other"])
    generate = st.sidebar.button("📊 Generate Analysis")

    if generate:
        data = {
            "ativo_circulante": ativo_circulante,
            "passivo_circulante": passivo_circulante,
            "estoques": estoques,
            "disponivel": disponivel,
            "passivo_total": passivo_total,
            "ativo_total": ativo_total,
            "lucro_liquido": lucro_liquido,
            "patrimonio_liquido": patrimonio_liquido,
            "fluxo_caixa_operacional": fluxo_caixa_operacional,
            "servico_divida": servico_divida,
            "ebitda": ebitda
        }
        indicators = calculate_indicators(data)
        rating, coverage_pct = classify_rating(indicators)
        accepted_value = valor_garantia * coverage_pct

        st.subheader("📊 Calculated Indicators")
        for name, value in indicators.items():
            st.markdown(f"**{name}: {value if value is not None else 'n/a'}**")

        st.subheader("📌 Final Rating")
        st.markdown(f"**Rating: {rating}**")
        st.markdown(f"**Suggested Limit: R$ {accepted_value:,.2f}**")
        st.markdown(f"🔒 Collateral Type: {tipo_garantia}")
        st.markdown(f"📉 Bank's Accepted Coverage: {coverage_pct * 100:.0f}%")

        st.subheader("📈 Indicator Bar Chart")
        fig_bar, ax = plt.subplots(figsize=(10, 5))
        ax.bar(indicators.keys(), [v if v is not None else 0 for v in indicators.values()])
        ax.set_xticks(range(len(indicators)))
        ax.set_xticklabels(indicators.keys(), rotation=30, ha="right")
        st.pyplot(fig_bar)

        st.markdown("This bar chart shows the individual distribution of each financial indicator. Higher liquidity and DSCR values indicate better financial health. High debt signals risk.")

        st.subheader("🕸️ Performance Radar")
        radar_vals = [
            normalize(indicators["Current Liquidity"], 0, 3),
            normalize(indicators["DSCR"], 0, 3),
            normalize(indicators["ROE"], 0, 0.3),
            normalize(1 - indicators["Total Debt Ratio"], 0, 1),
            normalize(indicators["Interest Coverage"], 0, 5),
        ]
        labels = ["Liquidity", "DSCR", "ROE", "Solvency", "Coverage"]
        radar_vals += radar_vals[:1]
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]
        fig_radar = plt.figure()
        ax = plt.subplot(111, polar=True)
        ax.plot(angles, radar_vals, "o-", linewidth=2)
        ax.fill(angles, radar_vals, alpha=0.25)
        ax.set_thetagrids(np.degrees(angles[:-1]), labels)
        st.pyplot(fig_radar)

        st.markdown("The radar chart summarizes the company's overall performance. Ideally, all areas should be evenly filled, indicating financial balance. Retracted areas suggest specific weaknesses.")

        st.subheader("🧐 Recommendations")
        recommendations = []
        if rating == "D": recommendations.append("❌ Avoid credit approval.")
        if rating == "C": recommendations.append("⚠️ Real collateral required.")
        if indicators["DSCR"] and indicators["DSCR"] < 1.2:
            recommendations.append("🔴 Limited payment capacity.")
        if recommendations:
            for r in recommendations:
                st.markdown(f"- {r}")
        else:
            st.markdown("No critical recommendations.")

        # Save chart images
        bar_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        fig_bar.savefig(bar_path.name, bbox_inches="tight")

        radar_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        fig_radar.savefig(radar_path.name, bbox_inches="tight")

        # Generate PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "Payment Capacity Analysis Report", ln=True)
        pdf.ln(5)
        for name, value in indicators.items():
            if value is not None:
                text = f"{name}: {value:.2f}".encode("latin-1", "ignore").decode("latin-1")
                pdf.cell(0, 8, text, ln=True)
        pdf.cell(0, 8, f"Rating: {rating}", ln=True)
        pdf.cell(0, 8, f"Suggested Limit: R$ {accepted_value:,.2f}", ln=True)
        for rec in recommendations:
            rec_text = f"- {rec}".encode("latin-1", "ignore").decode("latin-1")
            pdf.multi_cell(0, 8, rec_text)

        pdf.add_page()
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Indicator Bar Chart", ln=True)
        pdf.image(bar_path.name, x=10, y=25, w=180)

        pdf.add_page()
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Performance Radar", ln=True)
        pdf.image(radar_path.name, x=25, y=30, w=150)

        pdf_bytes = pdf.output(dest='S').encode("latin-1")
        st.download_button("📄 Click here to download the PDF", pdf_bytes, file_name="company_report.pdf")

with tabs[1]:
    st.subheader("📁 Batch Analysis via CSV")
    file = st.file_uploader("📤 Upload your CSV file", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.success("✅ File successfully loaded!")
        st.dataframe(df)

        for i, row in df.iterrows():
            st.markdown(f"### Company {i + 1}")
            indicators = calculate_indicators(row)
            rating, coverage_pct = classify_rating(indicators)
            accepted_value = row["valor_garantia"] * coverage_pct
            for name, value in indicators.items():
                st.markdown(f"**{name}: {value if value is not None else 'n/a'}**")
            st.markdown(f"**Rating: {rating}**")
            st.markdown(f"**Suggested Limit: R$ {accepted_value:,.2f}**")
            st.markdown("---")
