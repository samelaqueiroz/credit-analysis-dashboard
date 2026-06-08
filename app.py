"""
Dashboard de Análise de Crédito Bancário
Análise exploratória interativa de uma carteira de empréstimos
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Análise de Crédito",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5986 100%);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border-left: 4px solid #4fc3f7;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #4fc3f7; }
    .metric-label { font-size: 0.85rem; color: #b0bec5; margin-top: 4px; }
    .risk-high   { color: #ef5350; font-weight: bold; }
    .risk-medium { color: #ffa726; font-weight: bold; }
    .risk-low    { color: #66bb6a; font-weight: bold; }
    [data-testid="stSidebar"] { background-color: #0f2035; }
    h1, h2, h3 { color: #e3f2fd; }
</style>
""", unsafe_allow_html=True)


# ─── Carregamento de dados ─────────────────────────────────────────────────────
@st.cache_data
def carregar_dados():
<<<<<<< HEAD
    df = pd.read_csv("data/carteira_credito.csv")
=======
    df = pd.read_csv("carteira_credito.csv")
>>>>>>> 9e4f5209418a43d99a9e949d663d9b3828ac135a

    df["faixa_renda"] = pd.cut(
        df["renda_mensal"],
        bins=[0, 2000, 4000, 7000, 12000, 99999],
        labels=["Até R$2k", "R$2k–4k", "R$4k–7k", "R$7k–12k", "Acima R$12k"]
    )

    df["faixa_score"] = pd.cut(
        df["score_credito"],
        bins=[299, 500, 600, 700, 750, 851],
        labels=[
            "Muito Baixo\n(≤500)",
            "Baixo\n(501-600)",
            "Médio\n(601-700)",
            "Bom\n(701-750)",
            "Excelente\n(751+)"
        ]
    )

    df["faixa_idade"] = pd.cut(
        df["idade"],
        bins=[17, 25, 35, 45, 55, 75],
        labels=["18–25", "26–35", "36–45", "46–55", "56+"]
    )

    return df


df = carregar_dados()

# ─── Sidebar com filtros ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filtros")
    st.markdown("---")

    regioes = st.multiselect(
        "Região", options=df["regiao"].unique(),
        default=df["regiao"].unique()
    )

    contratos = st.multiselect(
        "Tipo de Contrato", options=df["tipo_contrato"].unique(),
        default=df["tipo_contrato"].unique()
    )

    faixa_score = st.slider(
        "Score de Crédito", int(df["score_credito"].min()),
        int(df["score_credito"].max()),
        (int(df["score_credito"].min()), int(df["score_credito"].max()))
    )

    faixa_renda = st.slider(
        "Renda Mensal (R$)", float(df["renda_mensal"].min()),
        float(df["renda_mensal"].max()),
        (float(df["renda_mensal"].min()), float(df["renda_mensal"].max())),
        format="R$ %.0f"
    )

    st.markdown("---")
    st.markdown("**Dataset:** Carteira sintética de 5.000 clientes  \n"
                "**Fonte:** Dados gerados com parâmetros de mercado brasileiro")

# Aplicar filtros
df_f = df[
    df["regiao"].isin(regioes) &
    df["tipo_contrato"].isin(contratos) &
    df["score_credito"].between(*faixa_score) &
    df["renda_mensal"].between(*faixa_renda)
]

# ─── Header ───────────────────────────────────────────────────────────────────
st.title("🏦 Dashboard de Análise de Crédito")
st.markdown("Exploração da carteira de empréstimos — perfil de risco, inadimplência e distribuições")
st.markdown("---")

# ─── KPIs principais ──────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)

taxa_inadimplencia = df_f["inadimplente"].mean() * 100
total_carteira = df_f["valor_emprestimo"].sum()
ticket_medio = df_f["valor_emprestimo"].mean()
score_medio = df_f["score_credito"].mean()
renda_media = df_f["renda_mensal"].mean()

with col1:
    st.metric("👥 Clientes", f"{len(df_f):,}".replace(",", "."))
with col2:
    st.metric("⚠️ Inadimplência", f"{taxa_inadimplencia:.1f}%",
              delta=f"{taxa_inadimplencia - df['inadimplente'].mean()*100:.1f}pp vs total",
              delta_color="inverse")
with col3:
    st.metric("💰 Carteira Total", f"R$ {total_carteira/1e6:.1f}M")
with col4:
    st.metric("🎯 Score Médio", f"{score_medio:.0f}")
with col5:
    st.metric("📊 Ticket Médio", f"R$ {ticket_medio:,.0f}".replace(",", "."))

st.markdown("---")

# ─── Linha 1: Inadimplência por perfil ────────────────────────────────────────
st.subheader("📉 Inadimplência por Perfil")
col1, col2, col3 = st.columns(3)

with col1:
    dados = df_f.groupby("historico_pagamentos")["inadimplente"].mean().mul(100).reset_index()
    dados.columns = ["Histórico", "Taxa (%)"]
    ordem = ["Excelente", "Bom", "Regular", "Ruim"]
    dados["Histórico"] = pd.Categorical(dados["Histórico"], categories=ordem, ordered=True)
    dados = dados.sort_values("Histórico")
    cores = ["#66bb6a", "#4fc3f7", "#ffa726", "#ef5350"]
    fig = px.bar(dados, x="Histórico", y="Taxa (%)", color="Histórico",
                 color_discrete_sequence=cores, title="Por Histórico de Pagamentos")
    fig.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    dados = df_f.groupby("tipo_contrato")["inadimplente"].mean().mul(100).reset_index()
    dados.columns = ["Contrato", "Taxa (%)"]
    dados = dados.sort_values("Taxa (%)", ascending=True)
    fig = px.bar(dados, x="Taxa (%)", y="Contrato", orientation="h",
                 color="Taxa (%)", color_continuous_scale="RdYlGn_r",
                 title="Por Tipo de Contrato")
    fig.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)", font_color="white",
                      coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col3:
    dados = df_f.groupby("regiao")["inadimplente"].mean().mul(100).reset_index()
    dados.columns = ["Região", "Taxa (%)"]
    fig = px.bar(dados.sort_values("Taxa (%)", ascending=False),
                 x="Região", y="Taxa (%)", color="Taxa (%)",
                 color_continuous_scale="RdYlGn_r", title="Por Região")
    fig.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)", font_color="white",
                      coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# ─── Linha 2: Score e Renda ───────────────────────────────────────────────────
st.subheader("📊 Distribuições e Correlações")
col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(
        df_f, x="score_credito", color="inadimplente",
        color_discrete_map={0: "#4fc3f7", 1: "#ef5350"},
        labels={"score_credito": "Score de Crédito", "inadimplente": "Inadimplente",
                "count": "Qtd"},
        title="Distribuição do Score por Status",
        barmode="overlay", opacity=0.75,
        category_orders={"inadimplente": [0, 1]}
    )
    fig.for_each_trace(lambda t: t.update(
        name="Adimplente" if t.name == "0" else "Inadimplente"
    ))
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                      font_color="white", legend_title="Status")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.scatter(
        df_f.sample(min(1000, len(df_f))),
        x="renda_mensal", y="score_credito",
        color=df_f.sample(min(1000, len(df_f)))["inadimplente"].map(
            {0: "Adimplente", 1: "Inadimplente"}),
        color_discrete_map={"Adimplente": "#4fc3f7", "Inadimplente": "#ef5350"},
        opacity=0.5, title="Score vs Renda Mensal",
        labels={"renda_mensal": "Renda Mensal (R$)", "score_credito": "Score",
                "color": "Status"}
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                      font_color="white")
    st.plotly_chart(fig, use_container_width=True)

# ─── Linha 3: Faixas e Escolaridade ──────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    dados = df_f.groupby("faixa_renda", observed=True)["inadimplente"].mean().mul(100).reset_index()
    dados.columns = ["Faixa de Renda", "Taxa (%)"]
    fig = px.bar(dados, x="Faixa de Renda", y="Taxa (%)",
                 color="Taxa (%)", color_continuous_scale="RdYlGn_r",
                 title="Inadimplência por Faixa de Renda")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                      font_color="white", coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    dados = df_f.groupby("escolaridade")["inadimplente"].mean().mul(100).reset_index()
    dados.columns = ["Escolaridade", "Taxa (%)"]
    ordem = ["Fundamental", "Médio", "Superior", "Pós-graduação"]
    dados["Escolaridade"] = pd.Categorical(dados["Escolaridade"], categories=ordem, ordered=True)
    dados = dados.sort_values("Escolaridade")
    fig = px.line(dados, x="Escolaridade", y="Taxa (%)", markers=True,
                  title="Inadimplência por Escolaridade",
                  color_discrete_sequence=["#4fc3f7"])
    fig.update_traces(line_width=3, marker_size=10)
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                      font_color="white")
    st.plotly_chart(fig, use_container_width=True)

# ─── Linha 4: Heatmap e Boxplot ───────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    pivot = df_f.groupby(["faixa_idade", "escolaridade"], observed=True)["inadimplente"] \
               .mean().mul(100).unstack(fill_value=0)
    fig = px.imshow(
        pivot,
        color_continuous_scale="RdYlGn_r",
        title="Heatmap: Inadimplência por Idade × Escolaridade",
        labels={"color": "Taxa (%)"},
        text_auto=".1f"
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.box(
        df_f, x="historico_pagamentos", y="taxa_juros_mensal",
        color="inadimplente",
        color_discrete_map={0: "#4fc3f7", 1: "#ef5350"},
        title="Taxa de Juros × Histórico de Pagamentos",
        labels={"taxa_juros_mensal": "Taxa de Juros (% a.m.)",
                "historico_pagamentos": "Histórico",
                "inadimplente": "Inadimplente"},
        category_orders={"historico_pagamentos": ["Excelente", "Bom", "Regular", "Ruim"]}
    )
    fig.for_each_trace(lambda t: t.update(
        name="Adimplente" if t.name == "0" else "Inadimplente"
    ))
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                      font_color="white")
    st.plotly_chart(fig, use_container_width=True)

# ─── Insights automáticos ─────────────────────────────────────────────────────
st.markdown("---")
st.subheader("💡 Insights da Carteira")

col1, col2, col3 = st.columns(3)

pior_regiao = df_f.groupby("regiao")["inadimplente"].mean().idxmax()
taxa_pior = df_f.groupby("regiao")["inadimplente"].mean().max() * 100

melhor_contrato = df_f.groupby("tipo_contrato")["inadimplente"].mean().idxmin()
taxa_melhor = df_f.groupby("tipo_contrato")["inadimplente"].mean().min() * 100

correlacao = df_f["score_credito"].corr(df_f["inadimplente"])

with col1:
    st.info(f"📍 **Maior risco regional:** {pior_regiao} com {taxa_pior:.1f}% de inadimplência")
with col2:
    st.success(f"✅ **Menor risco de contrato:** {melhor_contrato} com apenas {taxa_melhor:.1f}% de inadimplência")
with col3:
    st.warning(f"📉 **Correlação Score × Inadimplência:** {correlacao:.3f} — quanto menor o score, maior o risco")

# ─── Tabela de amostra ────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("🔎 Ver amostra dos dados"):
    st.dataframe(
        df_f.sample(min(50, len(df_f))).sort_values("score_credito"),
        use_container_width=True
    )
