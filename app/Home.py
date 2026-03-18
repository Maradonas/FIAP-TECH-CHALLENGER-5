from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Passos Mágicos | Tech Challenge 5",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(
    """
    <style>
    .block-container {padding-top: 1.4rem; padding-bottom: 2rem;}
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 0.9rem 1rem;
        border-radius: 16px;
    }
    .pm-hero {
        padding: 1.6rem 1.8rem;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(22,28,36,.95), rgba(17,52,94,.90));
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 1rem;
    }
    .pm-caption {color: #B8C4D6; font-size: 0.95rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="pm-hero">
        <h1 style="margin:0;">Passos Mágicos — Analytics & Risco de Defasagem</h1>
        <p class="pm-caption">
            Dashboard analítico e preditivo para responder às perguntas do case da FIAP Tech Challenge 5.
            Use a navegação lateral para acessar <b>Modelo</b> e <b>Análise Exploratória</b>.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1.3, 1])

with col1:
    st.subheader("Objetivo da aplicação")
    st.markdown(
        """
        Esta aplicação foi estruturada para sustentar uma apresentação gerencial e analítica, alinhada ao enunciado do case:
        evolução de desempenho, perfil de defasagem, relações entre indicadores, leitura por fase e um simulador de risco.
        """
    )
st.markdown("---")
st.subheader("Como navegar")
st.info(
    """
    **Modelo**: simulador preditivo de risco de defasagem.  
    **Análise Exploratória**: leitura visual dos indicadores do case, com filtros por ano e interpretação executiva.
    """
)
st.subheader("Principais conclusões")
st.markdown(
    """
    **1. Defasagem não deve ser inferida por regra simplista de IAN >= 1**  
    A lógica correta precisa respeitar a defasagem real (`defasagem < 0`) ou,
    na ausência dela, um fallback coerente. Isso evita distorções como 100% da base em risco.

    **2. O IAN precisa ser interpretado conforme a escala real da base**  
    Na base do case, os valores aparecem majoritariamente em `2.5`, `5` e `10`,
    então a classificação precisa refletir essa semântica:
    `2.5 = Severa`, `5 = Moderada`, `10 = Adequada`.

    **3. Engajamento, autoavaliação e desempenho devem ser lidos em conjunto**  
    Os gráficos da análise exploratória mostram se o aluno participa, como se percebe
    e qual é seu desempenho efetivo. Essa leitura integrada é mais útil para a banca
    do que mostrar médias isoladas.

    **4. O modelo preditivo só é confiável se treino e inferência usarem exatamente as mesmas features**  
    O simulador foi reduzido para refletir apenas as variáveis realmente esperadas
    pelo modelo salvo, eliminando incompatibilidades como `ipv` vs `ianv`.

    **5. A efetividade do programa deve ser argumentada com evolução ao longo do tempo**  
    Os blocos de IDA, INDE, fase e risco ajudam a mostrar se os alunos evoluem
    e se o programa parece reduzir vulnerabilidades ao longo dos anos.
    """
)

st.markdown("---")

