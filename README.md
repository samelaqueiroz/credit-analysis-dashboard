# 💳 Dashboard de Análise de Crédito Bancário

Dashboard interativo para análise exploratória de uma carteira de empréstimos, com foco em **perfil de inadimplência**, segmentação de risco e correlações entre variáveis financeiras e demográficas.

---

## Preview

> Dashboard com KPIs, gráficos interativos (Plotly) e filtros dinâmicos por região, tipo de contrato, score e renda.

---

## O que o dashboard analisa

- **Taxa de inadimplência** por região, tipo de contrato, escolaridade, faixa de renda e histórico de pagamentos
- **Distribuição do Score de Crédito** por status (adimplente vs inadimplente)
- **Correlação** entre renda mensal, score e inadimplência
- **Heatmap** de risco por cruzamento de idade e escolaridade
- **Boxplot** de taxa de juros por perfil de pagamento
- **Insights automáticos** gerados a partir dos filtros aplicados

---

## Estrutura

```
credit-analysis-dashboard/
│
├── app.py              # Dashboard principal (Streamlit)
├── gerar_dados.py      # Gerador de dataset sintético
├── requirements.txt
│
└── data/
    └── carteira_credito.csv   # Gerado pelo gerar_dados.py
```

---

## Stack

- **Streamlit** — interface web interativa
- **Pandas** — manipulação e agregação dos dados
- **Plotly** — gráficos interativos (barras, scatter, heatmap, boxplot, histograma)
- **NumPy** — geração dos dados sintéticos

---

## Sobre os dados

Dataset sintético com **5.000 clientes** gerado com parâmetros calibrados para refletir o mercado de crédito brasileiro:

| Variável | Descrição |
|---|---|
| `score_credito` | Score entre 300 e 850 |
| `renda_mensal` | Renda entre salário mínimo e R$30k |
| `taxa_juros_mensal` | Taxa entre 0.8% e 4.5% a.m. |
| `historico_pagamentos` | Excelente / Bom / Regular / Ruim |
| `inadimplente` | 0 = adimplente, 1 = inadimplente (target) |

---

## 📄 Licença

MIT
