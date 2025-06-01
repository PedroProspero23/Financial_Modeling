# app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile
import io

st.set_page_config(page_title="Análise de Capacidade de Pagamento - Setor Agro", layout="wide")
st.title("🏦 Análise de Capacidade de Pagamento Empresarial")

abas = st.tabs(["📋 Formulário Manual", "📁 Importar CSV em Lote"])

# Funções auxiliares
def safe_div(n, d):
    return round(n / d, 2) if d else None

def normaliza(v, mi, ma):
    return max(0, min((v - mi) / (ma - mi), 1)) if v is not None else 0

def calcular_indicadores(row):
    indicadores = {}
    indicadores["Liquidez Corrente"] = safe_div(row["ativo_circulante"], row["passivo_circulante"])
    indicadores["Liquidez Seca"] = safe_div(row["ativo_circulante"] - row["estoques"], row["passivo_circulante"])
    indicadores["Liquidez Imediata"] = safe_div(row["disponivel"], row["passivo_circulante"])
    indicadores["Endividamento Geral"] = safe_div(row["passivo_total"], row["ativo_total"])
    indicadores["ROE"] = safe_div(row["lucro_liquido"], row["patrimonio_liquido"])
    indicadores["DSCR"] = safe_div(row["fluxo_caixa_operacional"], row["servico_divida"])
    indicadores["Cobertura Juros"] = safe_div(row["ebitda"], row["servico_divida"])
    return indicadores

def classificar_rating(ind):
    score = 0
    if ind["Liquidez Corrente"] is not None:
        score += 3 if ind["Liquidez Corrente"] >= 1.5 else 2 if ind["Liquidez Corrente"] >= 1 else 1
    if ind["Endividamento Geral"] is not None:
        score += 3 if ind["Endividamento Geral"] <= 0.5 else 2 if ind["Endividamento Geral"] <= 0.7 else 1
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

# Variável para armazenar o PDF
pdf_bytes = None

with abas[0]:
    st.sidebar.header("📋 Dados Financeiros da Empresa")
    receita_total = st.sidebar.number_input("Receita líquida anual (R$)", 0.0, step=1000.0)
    lucro_liquido = st.sidebar.number_input("Lucro líquido anual (R$)", 0.0, step=1000.0)
    ativo_circulante = st.sidebar.number_input("Ativo circulante (R$)", 0.0, step=1000.0)
    passivo_circulante = st.sidebar.number_input("Passivo circulante (R$)", 0.0, step=1000.0)
    estoques = st.sidebar.number_input("Estoques (R$)", 0.0, step=1000.0)
    disponivel = st.sidebar.number_input("Disponibilidades (R$)", 0.0, step=1000.0)
    ativo_total = st.sidebar.number_input("Ativo total (R$)", 0.0, step=1000.0)
    passivo_total = st.sidebar.number_input("Passivo total (R$)", 0.0, step=1000.0)
    patrimonio_liquido = st.sidebar.number_input("Patrimônio líquido (R$)", 0.0, step=1000.0)
    servico_divida = st.sidebar.number_input("Serviço da dívida anual (R$)", 0.0, step=1000.0)
    ebitda = st.sidebar.number_input("EBITDA anual (R$)", 0.0, step=1000.0)
    fluxo_caixa_operacional = st.sidebar.number_input("Fluxo de caixa operacional (R$)", 0.0, step=1000.0)
    valor_garantia = st.sidebar.number_input("Valor da garantia (R$)", 0.0, step=1000.0)
    tipo_garantia = st.sidebar.selectbox("Tipo de garantia", ["Imóvel", "Equipamento", "Veículo", "Outro"])
    gerar = st.sidebar.button("📊 Gerar Análise")

    if gerar:
        dados = {
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
        indicadores = calcular_indicadores(dados)
        rating, percentual_cobertura = classificar_rating(indicadores)
        valor_aceito = valor_garantia * percentual_cobertura

        st.subheader("📊 Indicadores Calculados")
        for nome, valor in indicadores.items():
            st.markdown(f"**{nome}: {valor if valor is not None else 'n/d'}**")

        st.subheader("📌 Rating Final")
        st.markdown(f"**Rating: {rating}**")
        st.markdown(f"**Limite Sugerido: R$ {valor_aceito:,.2f}**")
        st.markdown(f"🔒 Tipo de Garantia: {tipo_garantia}")
        st.markdown(f"📉 Cobertura Aceita pelo Banco: {percentual_cobertura * 100:.0f}%")

        st.subheader("📈 Gráfico de Indicadores")
        fig_bar, ax = plt.subplots(figsize=(10, 5))
        ax.bar(indicadores.keys(), [v if v is not None else 0 for v in indicadores.values()])
        ax.set_xticks(range(len(indicadores)))
        ax.set_xticklabels(indicadores.keys(), rotation=30, ha="right")
        st.pyplot(fig_bar)

        st.markdown("Este gráfico de barras mostra a distribuição individual de cada indicador financeiro. Quanto maiores os valores de liquidez e DSCR, melhor a saúde financeira da empresa. Endividamento elevado indica risco.")

        st.subheader("🕸️ Radar de Performance")
        radar_vals = [
            normaliza(indicadores["Liquidez Corrente"], 0, 3),
            normaliza(indicadores["DSCR"], 0, 3),
            normaliza(indicadores["ROE"], 0, 0.3),
            normaliza(1 - indicadores["Endividamento Geral"], 0, 1),
            normaliza(indicadores["Cobertura Juros"], 0, 5),
        ]
        labels = ["Liquidez", "DSCR", "ROE", "Solvência", "Cobertura"]
        radar_vals += radar_vals[:1]
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]
        fig_radar = plt.figure()
        ax = plt.subplot(111, polar=True)
        ax.plot(angles, radar_vals, "o-", linewidth=2)
        ax.fill(angles, radar_vals, alpha=0.25)
        ax.set_thetagrids(np.degrees(angles[:-1]), labels)
        st.pyplot(fig_radar)

        st.markdown("O radar resume a performance global da empresa. Idealmente, todas as áreas devem estar preenchidas de forma uniforme, indicando equilíbrio financeiro. Pontas retraídas sugerem fragilidades específicas.")

        st.subheader("🧐 Recomendações")
        recomendacoes = []
        if rating == "D": recomendacoes.append("❌ Evitar concessão de crédito.")
        if rating == "C": recomendacoes.append("⚠️ Garantia real obrigatória.")
        if indicadores["DSCR"] and indicadores["DSCR"] < 1.2:
            recomendacoes.append("🔴 Capacidade de pagamento limitada.")
        if recomendacoes:
            for r in recomendacoes:
                st.markdown(f"- {r}")
        else:
            st.markdown("Nenhuma recomendação crítica.")

        # Salvar imagens dos gráficos
        bar_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        fig_bar.savefig(bar_path.name, bbox_inches="tight")

        radar_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        fig_radar.savefig(radar_path.name, bbox_inches="tight")

        # Geração de PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "Relatório de Análise de Capacidade de Pagamento", ln=True)
        pdf.ln(5)
        for nome, valor in indicadores.items():
            if valor is not None:
                texto = f"{nome}: {valor:.2f}".encode("latin-1", "ignore").decode("latin-1")
                pdf.cell(0, 8, texto, ln=True)
        pdf.cell(0, 8, f"Rating: {rating}", ln=True)
        pdf.cell(0, 8, f"Limite Sugerido: R$ {valor_aceito:,.2f}", ln=True)
        for rec in recomendacoes:
            texto_rec = f"- {rec}".encode("latin-1", "ignore").decode("latin-1")
            pdf.multi_cell(0, 8, texto_rec)

        pdf.add_page()
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Gráfico de Indicadores", ln=True)
        pdf.image(bar_path.name, x=10, y=25, w=180)

        pdf.add_page()
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "Radar de Performance", ln=True)
        pdf.image(radar_path.name, x=25, y=30, w=150)

        pdf_bytes = pdf.output(dest='S').encode("latin-1")
        st.download_button("📄 Clique aqui para baixar o PDF", pdf_bytes, file_name="relatorio_agro.pdf")

with abas[1]:
    st.subheader("📁 Análise em Lote via CSV")
    arquivo = st.file_uploader("📤 Selecione o arquivo CSV", type=["csv"])

    if arquivo:
        df = pd.read_csv(arquivo)
        st.success("✅ Arquivo carregado com sucesso!")
        st.dataframe(df)

        for i, row in df.iterrows():
            st.markdown(f"### Empresa {i + 1}")
            indicadores = calcular_indicadores(row)
            rating, percentual_cobertura = classificar_rating(indicadores)
            valor_aceito = row["valor_garantia"] * percentual_cobertura
            for nome, valor in indicadores.items():
                st.markdown(f"**{nome}: {valor if valor is not None else 'n/d'}**")
            st.markdown(f"**Rating: {rating}**")
            st.markdown(f"**Limite Sugerido: R$ {valor_aceito:,.2f}**")
            st.markdown("---")
