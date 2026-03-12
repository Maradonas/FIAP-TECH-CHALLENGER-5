import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os

# ----------------------------
# Configuração da página
# ----------------------------
st.set_page_config(
    page_title="Passos Mágicos • Risco de Defasagem",
    layout="centered"
)

st.title("Predição de Risco de Defasagem")
st.write(
    "Esta aplicação estima a probabilidade de um aluno entrar em **risco de defasagem**, "
    "com base em indicadores educacionais, comportamentais e psicossociais."
)

# ----------------------------
# Carregar modelo
# ----------------------------
MODEL_PATH = os.path.join("models", "modelo_risco_defasagem.joblib")

if not os.path.exists(MODEL_PATH):
    st.error("Modelo não encontrado. Execute o Notebook 02 e gere o arquivo .joblib.")
    st.stop()

model = joblib.load(MODEL_PATH)

# ----------------------------
# Inputs do usuário
# ----------------------------
st.subheader("Indicadores do aluno")

ida = st.slider("IDA — Desempenho acadêmico", 0.0, 10.0, 6.0, 0.1)
ieg = st.slider("IEG — Engajamento", 0.0, 10.0, 6.0, 0.1)
ips = st.slider("IPS — Psicossocial", 0.0, 10.0, 6.0, 0.1)
ipp = st.slider("IPP — Psicopedagógico", 0.0, 10.0, 6.0, 0.1)
iaa = st.slider("IAA — Autoavaliação", 0.0, 10.0, 6.0, 0.1)

# ----------------------------
# Predição
# ----------------------------
if st.button("Prever risco"):
    X = pd.DataFrame([{
        "ida": ida,
        "ieg": ieg,
        "ips": ips,
        "ipp": ipp,
        "iaa": iaa
    }])

    prob_risco = model.predict_proba(X)[0][1]

    st.metric(
        label="Probabilidade de risco de defasagem",
        value=f"{prob_risco:.2%}"
        )

    # detectar indicadores críticos
    indicadores = {
        "IDA (Desempenho)": ida,
        "IEG (Engajamento)": ieg,
        "IPS (Psicossocial)": ips,
        "IPP (Psicopedagógico)": ipp,
        "IAA (Autoavaliação)": iaa
    }

    criticos = [k for k, v in indicadores.items() if v <= 3]

    # interpretação do risco
    if prob_risco >= 0.65:
        st.error("🔴 Risco alto de defasagem.")
        st.write("**Ação recomendada:** intervenção pedagógica e psicossocial imediata.")

    elif prob_risco >= 0.35:
        st.warning("🟡 Risco moderado de defasagem.")
        st.write("**Ação recomendada:** acompanhamento próximo e reforço preventivo.")

    else:
        st.success("🟢 Risco baixo no momento.")
        st.write("**Ação recomendada:** manter acompanhamento regular.")

        if criticos:
            st.info(
                "⚠️ **Atenção:** apesar do risco global baixo, "
                "há indicadores críticos isolados que merecem atenção:\n\n"
                + ", ".join(criticos)
            )

    st.caption(
        "⚠️ Esta previsão é um apoio à decisão e deve ser analisada "
        "em conjunto com a equipe pedagógica."
    )
