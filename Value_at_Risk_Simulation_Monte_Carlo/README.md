# Value at Risk (VaR) using Monte Carlo Simulation

This project estimates the **Value at Risk (VaR)** of a financial portfolio using a **Monte Carlo simulation** approach. It models the uncertainty of daily returns based on a Gaussian distribution, and calculates potential losses over a short-term horizon.

---

# Objective

Estimate the potential monetary loss of a R$1,000,000 portfolio over a 10-day horizon, at a 95% confidence level, using **probabilistic simulation** instead of historical data.

---

# Methodology

- Simulate `n = 100,000` possible 10-day returns using a **normal distribution**
- Assume annual expected return and volatility:
  - Expected Return: 8% p.a.
  - Volatility: 20% p.a.
- Convert parameters to **daily basis** assuming 252 trading days/year
- Compute the 95th percentile of the **loss distribution** → this is the **VaR**

---

# Key Parameters

```python
valor_carteira = 1_000_000        # Portfolio value in BRL
retorno_esperado_anual = 0.08     # 8% expected annual return
volatilidade_anual = 0.20         # 20% annual volatility
dias = 10                         # Time horizon: 10 business days
nivel_confianca = 0.95            # Confidence level: 95%
n_simulacoes = 100_000            # Number of Monte Carlo simulations
