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
            Este dashboard foi desenvolvido para transformar os dados do case em uma leitura clara,
            visual e estratégica sobre desempenho, defasagem e evolução dos alunos ao longo do programa.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1.3, 1])

with col1:
    st.subheader("O que esta aplicação permite analisar")
    st.markdown(
        """
        A proposta deste painel é mostrar, de forma integrada, como diferentes dimensões da jornada do aluno
        se relacionam entre si.

        Ao longo da análise, observamos como o **desempenho acadêmico** se conecta com o **engajamento**,
        com a **autoavaliação**, com fatores **psicossociais** e com indicadores de **defasagem**.
        Dessa forma, o dashboard não mostra apenas números isolados: ele ajuda a contar a história
        do desenvolvimento do aluno dentro do programa.
        """
    )

with col2:
    st.subheader("Como interpretar o painel")
    st.markdown(
        """
        A navegação foi organizada em dois blocos principais:

        - **Modelo**: estima a probabilidade de risco de defasagem com base nos indicadores do aluno.
        - **Análise Exploratória**: apresenta os padrões, comparações e relações mais importantes da base.

        A leitura ideal começa pela visão analítica e depois avança para o simulador preditivo.
        """
    )

st.markdown("---")

st.subheader("Storytelling dos dados")
st.markdown(
    """
    Ao observar os indicadores em conjunto, o dashboard ajuda a responder uma pergunta central do case:
    **quais sinais ajudam a identificar alunos com maior vulnerabilidade acadêmica e como isso evolui ao longo do tempo?**

    A análise mostra que o aluno não deve ser avaliado apenas pelo desempenho final.
    Indicadores como **engajamento**, **autoavaliação** e aspectos **psicossociais** ajudam a explicar
    por que alguns alunos apresentam trajetórias mais consistentes, enquanto outros demonstram maior risco de defasagem.

    Também é possível perceber que a evolução do aluno precisa ser lida dentro do contexto do programa.
    Por isso, a comparação entre **anos**, **fases** e **níveis de desenvolvimento** é essencial para entender
    se há sinais de progressão ao longo da jornada educacional.
    """
)

st.subheader("Principais leituras do dashboard")
st.markdown(
    """
    **1. Engajamento e desempenho devem ser analisados juntos**  
    Quando o aluno participa mais, tende a existir uma trajetória mais favorável de desempenho.
    Isso torna o engajamento um dos sinais mais importantes para acompanhamento preventivo.

    **2. A percepção do aluno sobre si mesmo também importa**  
    Comparar autoavaliação com desempenho real ajuda a entender se o aluno reconhece sua própria evolução
    ou se existem sinais de desalinhamento que merecem atenção.

    **3. O risco de defasagem é multifatorial**  
    Ele não depende de um único indicador. Surge da combinação entre desempenho, adequação de nível,
    aspectos emocionais, engajamento e contexto pedagógico.

    **4. A leitura por fase e por ano ajuda a entender evolução**  
    Comparar grupos ao longo do tempo fortalece a análise sobre desenvolvimento
    e permite discutir indícios de efetividade do programa de forma mais consistente.

    **5. O modelo preditivo complementa a análise exploratória**  
    Depois de entender os padrões da base, o simulador permite transformar esses sinais
    em uma estimativa objetiva de risco, apoiando decisões de acompanhamento e priorização.
    """
)

st.markdown("---")

st.subheader("Como navegar")
st.info(
    """
    **Modelo**: simula a probabilidade de risco de defasagem a partir dos indicadores do aluno.  
    **Análise Exploratória**: apresenta os gráficos, comparações e interpretações que ajudam a explicar os padrões da base.
    """
)