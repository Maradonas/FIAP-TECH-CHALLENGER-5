from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

PALETTE = {
    "bg": "#0f172a",
    "panel": "#111827",
    "text": "#E5E7EB",
    "muted": "#94A3B8",
    "blue": "#38BDF8",
    "cyan": "#22D3EE",
    "green": "#34D399",
    "yellow": "#FBBF24",
    "orange": "#FB923C",
    "red": "#F87171",
    "purple": "#A78BFA",
}

CATEGORY_ORDER_IAN = ["Adequada", "Leve", "Moderada", "Severa"]
RISK_LABELS = {0: "Sem risco", 1: "Em risco"}


def tema(fig, height: int = 430):
    fig.update_layout(
        template="plotly_dark",
        title_x=0.01,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=60, b=20),
        legend_title_text="",
        font=dict(color=PALETTE["text"]),
        height=height,
        hovermode="closest",
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)")
    return fig



def barras_ian(df: pd.DataFrame):
    if "faixa_ian" not in df.columns:
        return None

    base = (
        df["faixa_ian"]
        .fillna("Não informado")
        .value_counts()
        .rename_axis("faixa_ian")
        .reset_index(name="quantidade")
    )
    base["ordem"] = base["faixa_ian"].map({v: i for i, v in enumerate(CATEGORY_ORDER_IAN)})
    base = base.sort_values(["ordem", "faixa_ian"], na_position="last")

    fig = px.bar(
        base,
        x="faixa_ian",
        y="quantidade",
        color="faixa_ian",
        text="quantidade",
        title="Perfil geral de defasagem (IAN)",
        color_discrete_map={
            "Adequada": PALETTE["green"],
            "Leve": PALETTE["yellow"],
            "Moderada": PALETTE["orange"],
            "Severa": PALETTE["red"],
            "Não informado": PALETTE["muted"],
        },
    )
    fig.update_traces(textposition="outside")
    return tema(fig)



def barras_ian_por_ano(df: pd.DataFrame):
    if not {"ano", "faixa_ian"}.issubset(df.columns):
        return None
    base = (
        df.dropna(subset=["ano", "faixa_ian"])
        .groupby(["ano", "faixa_ian"], as_index=False)
        .size()
        .rename(columns={"size": "quantidade"})
    )
    fig = px.bar(
        base,
        x="ano",
        y="quantidade",
        color="faixa_ian",
        barmode="stack",
        title="Evolução do perfil de defasagem por ano",
        category_orders={"faixa_ian": CATEGORY_ORDER_IAN},
        color_discrete_map={
            "Adequada": PALETTE["green"],
            "Leve": PALETTE["yellow"],
            "Moderada": PALETTE["orange"],
            "Severa": PALETTE["red"],
        },
    )
    return tema(fig)



def linha_media_por_ano(df: pd.DataFrame, coluna: str, titulo: str):
    if coluna not in df.columns or "ano" not in df.columns:
        return None
    base = df.dropna(subset=["ano", coluna]).groupby("ano", as_index=False)[coluna].mean()
    fig = px.line(base, x="ano", y=coluna, markers=True, title=titulo)
    fig.update_traces(line=dict(width=3), marker=dict(size=9))
    return tema(fig)



def linha_media_por_ano_e_grupo(df: pd.DataFrame, coluna: str, grupo: str, titulo: str):
    if not {"ano", coluna, grupo}.issubset(df.columns):
        return None
    base = df.dropna(subset=["ano", coluna, grupo]).groupby(["ano", grupo], as_index=False)[coluna].mean()
    fig = px.line(base, x="ano", y=coluna, color=grupo, markers=True, title=titulo)
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    return tema(fig)



def boxplot_por_fase(df: pd.DataFrame, coluna: str, titulo: str):
    fase_col = None
    for c in ["pedra", "fase", "nome_fase"]:
        if c in df.columns:
            fase_col = c
            break
    if not fase_col or coluna not in df.columns:
        return None
    fig = px.box(df.dropna(subset=[fase_col, coluna]), x=fase_col, y=coluna, color=fase_col, title=titulo)
    return tema(fig)



def scatter_relacao(df: pd.DataFrame, x: str, y: str, titulo: str, color: str | None = "ano"):
    if x not in df.columns or y not in df.columns:
        return None

    hover = [c for c in ["nome", "ra", "ano", "pedra", "inde", "faixa_ian"] if c in df.columns]
    color_col = color if color in df.columns else None
    base = df.dropna(subset=[x, y]).copy()

    fig = px.scatter(
        base,
        x=x,
        y=y,
        color=color_col,
        opacity=0.62,
        title=titulo,
        hover_data=hover,
    )

    if len(base) >= 2:
        try:
            coeffs = np.polyfit(base[x].astype(float), base[y].astype(float), 1)
            x_line = np.linspace(base[x].min(), base[x].max(), 100)
            y_line = coeffs[0] * x_line + coeffs[1]
            fig.add_trace(
                go.Scatter(
                    x=x_line,
                    y=y_line,
                    mode="lines",
                    name="Tendência linear",
                    line=dict(width=3, dash="dash", color=PALETTE["yellow"]),
                )
            )
        except Exception:
            pass

    return tema(fig)



def barras_risco_por_ano(df: pd.DataFrame):
    if not {"ano", "risco_defasagem"}.issubset(df.columns):
        return None
    base = df.dropna(subset=["ano", "risco_defasagem"]).groupby("ano", as_index=False)["risco_defasagem"].mean()
    base["pct_risco"] = base["risco_defasagem"] * 100
    fig = px.bar(base, x="ano", y="pct_risco", text="pct_risco", title="Percentual de alunos em risco por ano")
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_yaxes(title="% em risco")
    return tema(fig)



def boxplot_por_risco(df: pd.DataFrame, coluna: str, titulo: str):
    if "risco_defasagem" not in df.columns or coluna not in df.columns:
        return None
    base = df.dropna(subset=["risco_defasagem", coluna]).copy()
    base["grupo_risco"] = base["risco_defasagem"].astype(int).map(RISK_LABELS)
    fig = px.box(
        base,
        x="grupo_risco",
        y=coluna,
        color="grupo_risco",
        title=titulo,
        color_discrete_map={"Sem risco": PALETTE["green"], "Em risco": PALETTE["red"]},
    )
    return tema(fig)



def heatmap_correlacao(df: pd.DataFrame):
    colunas = [c for c in ["ian", "ida", "ieg", "iaa", "ips", "ipp", "ipv", "ianv", "inde"] if c in df.columns]
    if len(colunas) < 2:
        return None
    corr = df[colunas].corr(numeric_only=True)
    fig = px.imshow(corr, text_auto=".2f", aspect="auto", title="Correlação entre os principais indicadores", color_continuous_scale="RdBu_r")
    return tema(fig, height=500)



def feature_importance(modelo, feature_names: list[str]):
    if modelo is None or not feature_names:
        return None
    model_step = modelo.named_steps.get("model") if hasattr(modelo, "named_steps") else modelo
    if not hasattr(model_step, "feature_importances_"):
        return None
    base = pd.DataFrame({"feature": feature_names, "importance": model_step.feature_importances_}).sort_values("importance", ascending=True)
    fig = px.bar(base, x="importance", y="feature", orientation="h", title="Importância das variáveis no modelo")
    return tema(fig, height=360)



def radar_medias_por_risco(df: pd.DataFrame, indicadores: list[str], titulo: str):
    cols = [c for c in indicadores if c in df.columns]
    if "risco_defasagem" not in df.columns or len(cols) < 3:
        return None
    base = df.dropna(subset=["risco_defasagem"]).copy()
    base["grupo_risco"] = base["risco_defasagem"].astype(int).map(RISK_LABELS)
    resumo = base.groupby("grupo_risco", as_index=False)[cols].mean()
    fig = go.Figure()
    for _, row in resumo.iterrows():
        fig.add_trace(go.Scatterpolar(r=[row[c] for c in cols], theta=cols, fill="toself", name=row["grupo_risco"]))
    fig.update_layout(title=titulo, polar=dict(radialaxis=dict(visible=True)))
    return tema(fig, height=460)
