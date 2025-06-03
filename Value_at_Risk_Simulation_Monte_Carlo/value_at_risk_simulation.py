import numpy as np
import matplotlib.pyplot as plt

# === 1. INPUT PARAMETERS ===

# Valor total investido
valor_carteira = 1_000_000  # R$

# Retorno esperado anual e volatilidade
retorno_esperado_anual = 0.08   # 8%
volatilidade_anual = 0.20       # 20%

# Horizonte de análise
dias = 10
nivel_confianca = 0.95

# Número de simulações Monte Carlo
n_simulacoes = 100_000

# === 2. CONVERSÃO PARA BASE DIÁRIA ===

# O mercado considera 252 dias úteis por ano
retorno_diario = retorno_esperado_anual / 252
volatilidade_diaria = volatilidade_anual / np.sqrt(252)

# === 3. SIMULAÇÃO DE RETORNOS ===

# Simula n retornos acumulados em 'dias'
retornos_simulados = np.random.normal(
    loc=retorno_diario * dias,
    scale=volatilidade_diaria * np.sqrt(dias),
    size=n_simulacoes
)

# Transforma os retornos simulados em perdas monetárias
valores_finais = valor_carteira * (1 + retornos_simulados)
perdas_simuladas = valor_carteira - valores_finais  # Perda positiva = prejuízo

# === 4. CÁLCULO DO VALUE AT RISK ===

# Percentil de perda (ex: 5% das piores perdas)
VaR = np.percentile(perdas_simuladas, 100 * nivel_confianca)

# === 5. VISUALIZAÇÃO ===

plt.figure(figsize=(10, 6))
plt.hist(perdas_simuladas, bins=100, color='lightgray', edgecolor='black')
plt.axvline(VaR, color='red', linestyle='--', linewidth=2,
            label=f'VaR ({int(nivel_confianca*100)}%) = R$ {VaR:,.2f}')
plt.title("📉 Monte Carlo Simulation of Portfolio Losses")
plt.xlabel("Simulated Loss (R$)")
plt.ylabel("Frequency")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()
