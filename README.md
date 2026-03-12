# Datathon Passos Mágicos --- Fase 5

Projeto de **Data Analytics + Machine Learning** desenvolvido para o
case da **Associação Passos Mágicos**, com foco em análise dos
indicadores educacionais de 2022, 2023 e 2024 e na construção de um
**modelo preditivo de risco de defasagem escolar**.

## Objetivo

A proposta do Datathon é transformar dados educacionais em recomendações
acionáveis para apoiar a Passos Mágicos na identificação de padrões de
desempenho, engajamento e vulnerabilidade dos alunos.

O projeto foi estruturado em duas frentes principais:

-   **Análise exploratória e storytelling** para responder às perguntas
    de negócio do case.
-   **Modelagem preditiva** para estimar a probabilidade de um aluno
    entrar em risco de defasagem.

## Estrutura do projeto

``` bash
.
├── 01_EDA_Passos_Magicos.ipynb
├── 02_Modelo_Risco_Defasagem.ipynb
├── app.py
├── data_loader.py
├── preprocess.py
├── teste.py
├── models/
│   └── modelo_risco_defasagem.joblib
├── data/
│   └── BASE DE DADOS PEDE 2024 - DATATHON.xlsx
└── README.md
```

## Arquivos do projeto

### `01_EDA_Passos_Magicos.ipynb`

Notebook de análise exploratória dos dados.

Responsável por:

-   carregar e consolidar os dados dos anos de 2022, 2023 e 2024;
-   analisar os indicadores educacionais;
-   responder às perguntas analíticas do Datathon;
-   gerar insights e base para o storytelling da apresentação.

### `02_Modelo_Risco_Defasagem.ipynb`

Notebook de machine learning.

Responsável por:

-   preparar os dados para modelagem;
-   definir a variável alvo de risco de defasagem;
-   selecionar features;
-   treinar e avaliar o modelo;
-   salvar o modelo treinado em arquivo `.joblib`.

### `data_loader.py`

Módulo responsável por ler o arquivo Excel com múltiplas abas
(`PEDE2022`, `PEDE2023`, `PEDE2024`).

### `preprocess.py`

Módulo de pré-processamento responsável por:

-   padronizar nomes de colunas;
-   converter colunas numéricas;
-   adicionar coluna de ano;
-   unificar os dataframes;
-   detectar colunas-chave automaticamente;
-   criar o target de risco.

### `app.py`

Aplicação em **Streamlit** que disponibiliza o modelo preditivo para uso
operacional.

A interface permite informar os principais indicadores do aluno e obter:

-   probabilidade de risco de defasagem;
-   classificação do risco;
-   recomendação de ação.

### `teste.py`

Script auxiliar para validar a carga e a união dos dados.

## Indicadores analisados

-   **IAN** --- Índice de Adequação de Nível\
-   **IDA** --- Índice de Desempenho Acadêmico\
-   **IEG** --- Índice de Engajamento\
-   **IAA** --- Índice de Autoavaliação\
-   **IPS** --- Índice Psicossocial\
-   **IPP** --- Índice Psicopedagógico\
-   **IPV** --- Índice de Ponto de Virada\
-   **INDE** --- Índice de Desenvolvimento Educacional

## Requisitos

``` bash
pip install pandas numpy scikit-learn streamlit joblib openpyxl matplotlib seaborn
```

## Como executar

``` bash
python teste.py
jupyter notebook 01_EDA_Passos_Magicos.ipynb
jupyter notebook 02_Modelo_Risco_Defasagem.ipynb
streamlit run app.py
```

------------------------------------------------------------------------

# Resultados Obtidos

A análise exploratória revelou padrões relevantes entre os indicadores
educacionais.

Principais observações:

-   **IEG (engajamento)** apresentou correlação positiva com **IDA
    (desempenho)**.
-   Indicadores psicossociais (**IPS**) mais baixos tendem a anteceder
    queda de desempenho.
-   A combinação de **IDA + IEG + IPS + IPP** mostrou forte relação com
    **INDE**.

## Modelo Preditivo

Foi desenvolvido um modelo utilizando **Random Forest Classifier**.

Features utilizadas:

-   IDA\
-   IEG\
-   IPS\
-   IPP\
-   IAA

O modelo apresentou desempenho consistente para identificação de risco
de defasagem, superando o baseline nas métricas de classificação.

Métricas avaliadas:

-   Accuracy
-   Precision
-   Recall
-   F1-score
-   ROC-AUC

## Aplicação

Foi desenvolvida uma aplicação em **Streamlit** para permitir simulação
de risco de defasagem a partir dos indicadores do aluno.

A aplicação permite:

-   inserir indicadores do aluno
-   calcular probabilidade de risco
-   classificar risco em **baixo, moderado ou alto**
-   apoiar intervenções pedagógicas preventivas

------------------------------------------------------------------------

## Autor

Projeto desenvolvido para o **Datathon Passos Mágicos --- Fase 5**.
