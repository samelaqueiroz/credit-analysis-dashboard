"""
Gerador de dados sintéticos de crédito bancário.
Simula uma carteira realista com perfis de inadimplência típicos do mercado brasileiro.
Execute este script uma vez para gerar o arquivo data/carteira_credito.csv
"""

import pandas as pd
import numpy as np
import os

np.random.seed(42)
os.makedirs("data", exist_ok=True)

N = 5000

# ─── Variáveis demográficas ────────────────────────────────────────────────────
idade = np.random.normal(38, 11, N).clip(18, 75).astype(int)

escolaridade = np.random.choice(
    ["Fundamental", "Médio", "Superior", "Pós-graduação"],
    N, p=[0.15, 0.40, 0.35, 0.10]
)

estado_civil = np.random.choice(
    ["Solteiro", "Casado", "Divorciado", "Viúvo"],
    N, p=[0.35, 0.45, 0.15, 0.05]
)

regiao = np.random.choice(
    ["Sul", "Sudeste", "Centro-Oeste", "Nordeste", "Norte"],
    N, p=[0.15, 0.42, 0.12, 0.21, 0.10]
)

# ─── Variáveis financeiras ─────────────────────────────────────────────────────
renda_base = np.where(
    escolaridade == "Pós-graduação", np.random.normal(9000, 3000, N),
    np.where(escolaridade == "Superior", np.random.normal(5500, 2000, N),
    np.where(escolaridade == "Médio",    np.random.normal(2800, 1000, N),
                                          np.random.normal(1700, 600, N)))
).clip(1320, 30000)

renda_mensal = renda_base.round(2)

num_dependentes = np.random.choice([0, 1, 2, 3, 4], N, p=[0.30, 0.25, 0.28, 0.12, 0.05])

anos_emprego = np.random.exponential(4, N).clip(0, 35).round(1)

tipo_contrato = np.random.choice(
    ["CLT", "Autônomo", "Servidor Público", "Empresário"],
    N, p=[0.55, 0.20, 0.15, 0.10]
)

# ─── Variáveis do crédito ──────────────────────────────────────────────────────
valor_emprestimo = (renda_mensal * np.random.uniform(3, 18, N)).clip(1000, 150000).round(-2)

prazo_meses = np.random.choice([12, 24, 36, 48, 60, 72, 84], N,
                                p=[0.08, 0.15, 0.22, 0.20, 0.18, 0.12, 0.05])

taxa_juros = np.where(
    tipo_contrato == "Servidor Público", np.random.uniform(0.8, 1.5, N),
    np.where(tipo_contrato == "CLT",     np.random.uniform(1.2, 2.5, N),
    np.where(tipo_contrato == "Empresário", np.random.uniform(1.5, 3.0, N),
                                             np.random.uniform(2.0, 4.5, N)))
).round(2)

historico_pagamentos = np.random.choice(
    ["Excelente", "Bom", "Regular", "Ruim"],
    N, p=[0.30, 0.35, 0.22, 0.13]
)

score_credito = (
    500
    + (renda_mensal / 100).clip(0, 150)
    + anos_emprego * 5
    - num_dependentes * 10
    + np.where(historico_pagamentos == "Excelente", 150,
      np.where(historico_pagamentos == "Bom", 80,
      np.where(historico_pagamentos == "Regular", 0, -100)))
    + np.random.normal(0, 30, N)
).clip(300, 850).round(0).astype(int)

# ─── Variável target: inadimplência ───────────────────────────────────────────
prob_inadimplencia = (
    0.10
    - (score_credito - 550) * 0.0008
    + (taxa_juros - 2.0) * 0.03
    + num_dependentes * 0.02
    - anos_emprego * 0.005
    + np.where(historico_pagamentos == "Ruim", 0.25,
      np.where(historico_pagamentos == "Regular", 0.08, 0))
    + np.where(tipo_contrato == "Autônomo", 0.05, 0)
).clip(0.01, 0.90)

inadimplente = (np.random.uniform(0, 1, N) < prob_inadimplencia).astype(int)

# ─── Montar DataFrame ──────────────────────────────────────────────────────────
df = pd.DataFrame({
    "idade": idade,
    "escolaridade": escolaridade,
    "estado_civil": estado_civil,
    "regiao": regiao,
    "num_dependentes": num_dependentes,
    "tipo_contrato": tipo_contrato,
    "anos_emprego": anos_emprego,
    "renda_mensal": renda_mensal,
    "valor_emprestimo": valor_emprestimo,
    "prazo_meses": prazo_meses,
    "taxa_juros_mensal": taxa_juros,
    "historico_pagamentos": historico_pagamentos,
    "score_credito": score_credito,
    "inadimplente": inadimplente,
})

caminho = "data/carteira_credito.csv"
df.to_csv(caminho, index=False)

taxa = inadimplente.mean() * 100
print(f"✅ Dataset gerado: {len(df)} clientes")
print(f"   Taxa de inadimplência: {taxa:.1f}%")
print(f"   Salvo em: {caminho}")
