from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from utils.loaders import (
    load_model,
    load_metrics,
    get_model_features,
    build_model_input,
)
from utils.charts import feature_importance

BASE_DIR = Path(__file__).resolve().parents[1]
METRICS_PATH = BASE_DIR / "models" / "metricas_modelo.json"


def get_metric_value(metricas: dict, *possible_keys, default=None):
    for key in possible_keys:
        if key in metricas and metricas[key] is not None:
            return metricas[key]
    return default

st.title("Modelo Preditivo de Risco de Defasagem")

st.markdown("""
Esta página apresenta o **modelo preditivo de risco de defasagem**.

- O gráfico mostra **quais indicadores têm maior influência** na previsão do modelo.
- No **simulador de risco**, ajuste os valores dos indicadores para representar diferentes cenários.
- A probabilidade de risco será atualizada automaticamente com base nos valores escolhidos.

Use o simulador para explorar como mudanças nos indicadores podem impactar o risco estimado.
""")

modelo = load_model()
metricas = load_metrics()
features_modelo = get_model_features(modelo, metricas)

st.subheader("Importância das variáveis")
fig_importancia = feature_importance(modelo, features_modelo)
if fig_importancia is not None:
    st.plotly_chart(fig_importancia, width="stretch")
    st.caption(
        "As variáveis com maior importância são as que mais influenciam a classificação do modelo."
    )

st.subheader("Simulador de risco")


defaults = {
    "ida": 6.0,
    "ieg": 6.0,
    "iaa": 6.0,
    "ips": 6.0,
    "ipp": 6.0,
    "ian": 5.0,
    "ianv": 5.0,
    "ipv": 6.0,
    "inde": 6.0,
}

descricoes = {
    "ida": "Desempenho acadêmico do aluno.",
    "ieg": "Engajamento nas atividades.",
    "iaa": "Autoavaliação do próprio aluno.",
    "ips": "Indicadores psicossociais.",
    "ipp": "Indicadores psicopedagógicos.",
    "ian": "Adequação de nível.",
    "ianv": "Variável derivada usada em algumas versões do treino.",
    "ipv": "Indicador complementar do aluno.",
    "inde": "Indicador global do desenvolvimento educacional.",
}

entrada_usuario = {}
cols = st.columns(3)

for i, feature in enumerate(features_modelo):
    with cols[i % 3]:
        entrada_usuario[feature] = st.slider(
            feature.upper(),
            min_value=0.0,
            max_value=10.0,
            value=float(defaults.get(feature, 5.0)),
            step=0.1,
            help=descricoes.get(feature.lower(), "")
        )

if st.button("Calcular probabilidade de risco"):
    try:
        entrada = build_model_input(modelo, entrada_usuario)
        prob = modelo.predict_proba(entrada)[0][1]

        c1, c2 = st.columns([1, 2])
        c1.metric("Probabilidade de risco", f"{prob * 100:.1f}%")

        if prob < 0.33:
            c2.success("Classificação: Baixo risco")
        elif prob < 0.66:
            c2.warning("Classificação: Risco moderado")
        else:
            c2.error("Classificação: Alto risco")

        st.info(
            """
            Esta probabilidade representa a chance estimada de o aluno entrar
            em risco de defasagem segundo o padrão aprendido pelo modelo.
            """
        )

    except Exception as e:
        st.error(f"Erro ao calcular predição: {e}")