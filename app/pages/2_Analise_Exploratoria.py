import streamlit as st
import pandas as pd

from utils.loaders import load_base
from utils.charts import (
    barras_ian,
    linha_media_por_ano,
    scatter_relacao,
    boxplot_por_risco,
    boxplot_por_fase,
    heatmap_correlacao,
    barras_risco_por_ano,
)

try:
    import plotly.express as px
except ImportError:
    px = None


st.set_page_config(page_title="Análise Exploratória", layout="wide")


def bloco_interpretacao(titulo: str, texto: str):
    st.markdown(
        f"""
        <div style="
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            padding: 14px 16px;
            border-radius: 12px;
            margin-top: 8px;
            margin-bottom: 18px;
        ">
            <div style="font-weight: 700; margin-bottom: 6px;">{titulo}</div>
            <div style="font-size: 0.95rem; line-height: 1.5;">{texto}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def safe_metric(df: pd.DataFrame, col: str):
    if col in df.columns and df[col].notna().any():
        return float(df[col].mean())
    return None


def show_metric_card(col, label, value, suffix=""):
    if value is None:
        col.metric(label, "-")
    else:
        col.metric(label, f"{value:.2f}{suffix}")


def filtro_ano(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filtros")

    if "ano" not in df.columns:
        st.sidebar.warning("A coluna 'ano' não existe na base.")
        return df

    anos_validos = sorted([int(x) for x in df["ano"].dropna().unique().tolist()])

    if not anos_validos:
        st.sidebar.warning("Não há anos válidos para filtrar.")
        return df

    opcoes = ["Todos"] + anos_validos
    ano_selecionado = st.sidebar.selectbox("Selecione o ano", opcoes, index=0)

    if ano_selecionado == "Todos":
        return df

    return df[df["ano"] == ano_selecionado].copy()


def grafico_efetividade_fase_ano(df: pd.DataFrame):
    if px is None:
        return None

    if not {"fase", "ano", "inde"}.issubset(df.columns):
        return None

    base = (
        df.dropna(subset=["fase", "ano", "inde"])
        .groupby(["ano", "fase"], as_index=False)["inde"]
        .mean()
        .sort_values(["ano", "fase"])
    )

    if base.empty:
        return None

    fig = px.line(
        base,
        x="ano",
        y="inde",
        color="fase",
        markers=True,
        title="Evolução do INDE por fase e ano"
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=60, b=20),
        legend_title_text="Fase"
    )
    return fig


def grafico_distribuicao_inde_por_pedra(df: pd.DataFrame):
    if px is None:
        return None

    if not {"pedra", "inde"}.issubset(df.columns):
        return None

    base = df.dropna(subset=["pedra", "inde"]).copy()
    if base.empty:
        return None

    fig = px.box(
        base,
        x="pedra",
        y="inde",
        points="outliers",
        title="Distribuição do INDE por classificação PEDRA"
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis_title="PEDRA",
        yaxis_title="INDE"
    )
    return fig


def grafico_media_indicadores(df: pd.DataFrame):
    if px is None:
        return None

    indicadores = [c for c in ["ida", "ieg", "iaa", "ips", "ipp", "inde"] if c in df.columns]
    if not indicadores:
        return None

    medias = (
        df[indicadores]
        .mean()
        .reset_index()
    )
    medias.columns = ["indicador", "media"]

    fig = px.bar(
        medias,
        x="indicador",
        y="media",
        title="Média dos principais indicadores"
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis_title="Indicador",
        yaxis_title="Média"
    )
    return fig


# =========================
# CARREGAMENTO DA BASE
# =========================
st.title("Análise Exploratória")
st.markdown(
    """
    Esta página apresenta a leitura analítica da base do case Passos Mágicos, com foco em:
    desempenho, defasagem, engajamento, autoavaliação, aspectos psicossociais,
    risco de defasagem e sinais de efetividade do programa.
    """
)

df = load_base()
df_filtrado = filtro_ano(df)

if df_filtrado.empty:
    st.warning("Nenhum registro encontrado para o filtro selecionado.")
    st.stop()

# =========================
# KPIs
# =========================
st.subheader("Visão geral da base filtrada")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total de registros", f"{len(df_filtrado):,}".replace(",", "."))

media_ida = safe_metric(df_filtrado, "ida")
media_inde = safe_metric(df_filtrado, "inde")

risco_pct = None
if "risco_defasagem" in df_filtrado.columns and df_filtrado["risco_defasagem"].notna().any():
    risco_pct = float(df_filtrado["risco_defasagem"].mean() * 100)

show_metric_card(k2, "Média IDA", media_ida)
show_metric_card(k3, "Média INDE", media_inde)
show_metric_card(k4, "% em risco", risco_pct, "%")

bloco_interpretacao(
    "Leitura executiva",
    """
    Os KPIs acima oferecem uma visão rápida da amostra analisada. Eles ajudam a contextualizar
    os gráficos seguintes e mostram, de forma resumida, o volume da base, o desempenho médio,
    o desenvolvimento global e a proporção de alunos em risco de defasagem.
    """
)

# =========================
# BLOCO 1 - IAN
# =========================
st.subheader("1. Perfil geral de defasagem (IAN)")
fig = barras_ian(df_filtrado)
if fig is not None:
    st.plotly_chart(fig, width="stretch")
    bloco_interpretacao(
        "Como interpretar",
        """
        Este gráfico mostra a distribuição dos alunos nas faixas de adequação de nível.
        Concentração em faixas mais críticas sugere maior necessidade de recuperação pedagógica,
        enquanto maior presença em faixas adequadas indica menor defasagem.
        """
    )
else:
    st.info("Não foi possível gerar o gráfico de IAN com a base atual.")

# =========================
# BLOCO 2 - EVOLUÇÃO IDA
# =========================
st.subheader("2. Evolução do desempenho acadêmico (IDA)")
fig = linha_media_por_ano(df, "ida", "Evolução do IDA por ano")
if fig is not None:
    st.plotly_chart(fig, width="stretch")
    bloco_interpretacao(
        "Como interpretar",
        """
        Este gráfico responde se o desempenho acadêmico médio melhora, piora ou se mantém ao longo
        do tempo. Uma trajetória ascendente sugere avanço na aprendizagem; estabilidade ou queda
        podem indicar limitações na evolução dos alunos.
        """
    )
else:
    st.info("Não foi possível gerar a evolução do IDA.")

# =========================
# BLOCO 3 - IEG x IDA
# =========================
st.subheader("3. Relação entre engajamento (IEG) e desempenho (IDA)")
fig = scatter_relacao(df_filtrado, "ieg", "ida", "Relação entre IEG e IDA")
if fig is not None:
    st.plotly_chart(fig, width="stretch")
    bloco_interpretacao(
        "Como interpretar",
        """
        Este gráfico avalia se alunos mais engajados tendem a apresentar melhor desempenho.
        Quando a tendência é positiva, isso reforça a hipótese de que o engajamento contribui
        para melhores resultados acadêmicos.
        """
    )
else:
    st.info("Não foi possível gerar o gráfico IEG x IDA.")

# =========================
# BLOCO 4 - IAA x IDA
# =========================
st.subheader("4. Autoavaliação (IAA) versus desempenho real (IDA)")
fig = scatter_relacao(df_filtrado, "iaa", "ida", "Relação entre IAA e IDA")
if fig is not None:
    st.plotly_chart(fig, width="stretch")
    bloco_interpretacao(
        "Como interpretar",
        """
        Este gráfico compara a percepção do aluno sobre si mesmo com seu desempenho real.
        Quanto mais coerente for essa relação, maior o alinhamento entre autopercepção e resultado.
        """
    )
else:
    st.info("Não foi possível gerar o gráfico IAA x IDA.")

# =========================
# BLOCO 5 - IPS por risco
# =========================
st.subheader("5. IPS por grupo de risco")
fig = boxplot_por_risco(df_filtrado, "ips", "Distribuição de IPS por grupo de risco")
if fig is not None:
    st.plotly_chart(fig, width="stretch")
    bloco_interpretacao(
        "Como interpretar",
        """
        Este boxplot compara os indicadores psicossociais entre alunos em risco e fora de risco.
        Diferenças nas medianas e na dispersão sugerem que fatores psicossociais podem influenciar
        a trajetória escolar e a probabilidade de defasagem.
        """
    )
else:
    st.info("Não foi possível gerar o boxplot de IPS por risco.")

# =========================
# BLOCO 6 - IPP por risco
# =========================
st.subheader("6. IPP por grupo de risco")
fig = boxplot_por_risco(df_filtrado, "ipp", "Distribuição de IPP por grupo de risco")
if fig is not None:
    st.plotly_chart(fig, width="stretch")
    bloco_interpretacao(
        "Como interpretar",
        """
        Este gráfico mostra se o componente psicopedagógico se comporta de forma diferente
        entre os grupos de risco. Se os alunos em risco tiverem níveis piores de IPP,
        isso reforça seu valor analítico na explicação da defasagem.
        """
    )
else:
    st.info("Não foi possível gerar o boxplot de IPP por risco.")

# =========================
# BLOCO 7 - INDE por fase
# =========================
st.subheader("7. INDE por fase do programa")
fig = boxplot_por_fase(df_filtrado, "inde", "Distribuição do INDE por fase")
if fig is not None:
    st.plotly_chart(fig, width="stretch")
    bloco_interpretacao(
        "Como interpretar",
        """
        Este gráfico ajuda a entender se as fases do programa apresentam diferenças claras
        no desenvolvimento global dos alunos. Fases mais avançadas com medianas maiores
        sugerem progressão compatível com a proposta do programa.
        """
    )
else:
    st.info("Não foi possível gerar o gráfico de INDE por fase.")

# =========================
# BLOCO 8 - HEATMAP
# =========================
st.subheader("8. Correlação entre os principais indicadores")
fig = heatmap_correlacao(df_filtrado)
if fig is not None:
    st.plotly_chart(fig, width="stretch")
    bloco_interpretacao(
        "Como interpretar",
        """
        O heatmap resume como os indicadores se relacionam entre si. Correlações positivas mostram
        variáveis que crescem juntas; correlações negativas sugerem relações inversas.
        Esse bloco ajuda a contar a história da base de forma integrada.
        """
    )
else:
    st.info("Não foi possível gerar o heatmap de correlação.")

# =========================
# BLOCO 9 - RISCO POR ANO
# =========================
st.subheader("9. Evolução do risco de defasagem")
fig = barras_risco_por_ano(df)
if fig is not None:
    st.plotly_chart(fig, width="stretch")
    bloco_interpretacao(
        "Como interpretar",
        """
        Este gráfico mostra se a proporção de alunos em risco vem aumentando ou diminuindo ao longo
        dos anos. Queda do risco é um sinal favorável; crescimento do risco sugere necessidade de
        intervenção mais rápida e revisão das estratégias de acompanhamento.
        """
    )
else:
    st.info("Não foi possível gerar o gráfico de risco por ano.")

# =========================
# BLOCO 10 - INDE por fase e ano
# =========================
st.subheader("10. Efetividade do programa por fase e ano")
fig = grafico_efetividade_fase_ano(df)
if fig is not None:
    st.plotly_chart(fig, width="stretch")
    bloco_interpretacao(
        "Como interpretar",
        """
        Este é um dos blocos mais úteis para discutir efetividade do programa. Ele mostra como o INDE
        evolui ao longo do tempo dentro de cada fase. Uma tendência de melhora consistente fortalece
        a leitura de que o programa está promovendo avanço educacional.
        """
    )
else:
    st.info("Não foi possível gerar o gráfico de efetividade por fase e ano.")

# =========================
# BLOCO 11 - INDE por PEDRA
# =========================
st.subheader("11. Desenvolvimento global por classificação PEDRA")
fig = grafico_distribuicao_inde_por_pedra(df_filtrado)
if fig is not None:
    st.plotly_chart(fig, width="stretch")
    bloco_interpretacao(
        "Como interpretar",
        """
        Este bloco mostra como o INDE se distribui entre as classificações PEDRA.
        Ele ajuda a comunicar, de forma executiva, como os grupos de alunos se diferenciam
        em termos de desenvolvimento global.
        """
    )
else:
    st.info("Não foi possível gerar o gráfico de INDE por PEDRA.")

# =========================
# BLOCO 12 - MÉDIA DOS INDICADORES
# =========================
st.subheader("12. Comparação direta entre os principais indicadores")
fig = grafico_media_indicadores(df_filtrado)
if fig is not None:
    st.plotly_chart(fig, width="stretch")
    bloco_interpretacao(
        "Como interpretar",
        """
        Este gráfico resume a média dos principais indicadores da base filtrada.
        Ele é útil para a banca porque entrega uma visão direta de quais dimensões aparecem
        mais fortes ou mais frágeis no conjunto analisado.
        """
    )
else:
    st.info("Não foi possível gerar o gráfico de médias dos indicadores.")

# =========================
# TABELA FINAL
# =========================
st.subheader("Base filtrada")
st.dataframe(df_filtrado, width="stretch")