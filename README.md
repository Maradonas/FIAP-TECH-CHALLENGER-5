# FIAP Tech Challenge 5 --- Datathon Passos Mágicos

## Dashboard Analítico e Modelo Preditivo de Risco de Defasagem

## 1. Visão geral

Este projeto foi desenvolvido para o **FIAP Tech Challenge 5 / Datathon
Fase 5**, com base no case da **Associação Passos Mágicos**, organização
social que atua há mais de três décadas na transformação da vida de
crianças e jovens em vulnerabilidade social por meio da educação.

A proposta desta entrega foi construir uma solução completa composta
por:

-   análise exploratória de dados
-   modelo preditivo de risco de defasagem
-   dashboard interativo em Streamlit
-   pipeline de tratamento e preparação de dados

O objetivo principal é identificar **padrões e sinais que ajudam a
prever alunos com maior risco de defasagem escolar**.

------------------------------------------------------------------------

## 2. Objetivo do desafio

O Tech Challenge solicita:

-   análise exploratória com storytelling
-   construção de modelo preditivo
-   aplicação interativa em Streamlit
-   repositório GitHub com código e documentação
-   apresentação e vídeo explicando a solução

------------------------------------------------------------------------

## 3. Perguntas de negócio respondidas

O projeto foi estruturado para responder questões como:

-   Qual o perfil de defasagem dos alunos?
-   O engajamento influencia o desempenho?
-   Existe coerência entre autoavaliação e desempenho real?
-   Fatores psicossociais influenciam o risco?
-   Quais indicadores explicam melhor o desenvolvimento do aluno?
-   É possível prever risco de defasagem com machine learning?
-   Existem sinais de efetividade do programa ao longo do tempo?

------------------------------------------------------------------------

## 4. Base de dados

A base consolidada possui aproximadamente **3.030 registros**, cobrindo
os anos:

-   2022
-   2023
-   2024

Indicadores principais utilizados:

-   IDA --- desempenho acadêmico
-   IEG --- engajamento
-   IAA --- autoavaliação
-   IPS --- fatores psicossociais
-   IPP --- fatores psicopedagógicos
-   IPV --- ponto de virada
-   IAN --- adequação de nível
-   INDE --- desenvolvimento educacional global

------------------------------------------------------------------------

## 5. Preparação dos dados

O processo de preparação incluiu:

1.  consolidação das abas anuais do Excel
2.  padronização de nomes de colunas
3.  conversão de colunas numéricas
4.  unificação das bases
5.  criação da variável alvo de risco

------------------------------------------------------------------------

## 6. Definição do risco de defasagem

A variável alvo foi construída utilizando a regra:

risco_defasagem = 1 se defasagem \< 0

Fallbacks utilizados:

-   defas \< 0
-   aproximação via IAN \<= 5

Essa regra aproxima o conceito de **atraso em relação à fase ideal do
aluno**.

------------------------------------------------------------------------

## 7. Classificação de IAN

Faixas utilizadas:

\<= 2.5 → Severa\
\<= 5 → Moderada\
\< 10 → Leve\
\>= 10 → Adequada

------------------------------------------------------------------------

## 8. Estrutura do projeto

app/ Home.py pages/ 1_Modelo.py 2_Analise_Exploratoria.py utils/
loaders.py charts.py

data/ processed/ base_unificada.csv diagnostico_base.json

models/ modelo_risco_defasagem.joblib metricas_modelo.json

notebooks/ src/ README.md

------------------------------------------------------------------------

## 9. Dashboard

O dashboard possui três áreas principais:

Home → resumo executivo\
Análise exploratória → gráficos e insights\
Modelo → importância das variáveis e simulador de risco

------------------------------------------------------------------------

## 10. Modelo preditivo

O modelo utiliza aprendizado supervisionado para prever risco de
defasagem.

Principais features utilizadas:

-   ida
-   ieg
-   ips
-   ipp
-   iaa
-   ian
-   inde

------------------------------------------------------------------------

## 11. Resultados do modelo

Accuracy ≈ 0.978\
Precision = 1.00\
Recall ≈ 0.953\
F1 Score ≈ 0.976\
ROC AUC = 1.0

Esses resultados indicam alta capacidade de separação entre alunos em
risco e fora de risco.

------------------------------------------------------------------------

## 12. Feature Engineering

Foram criadas variáveis derivadas como:

-   média de indicadores
-   variação entre indicadores
-   indicadores compostos de desempenho

Essas variáveis ajudam a capturar **padrões mais complexos de
comportamento dos alunos**.

------------------------------------------------------------------------

## 13. Insights principais

A análise sugere que:

-   risco de defasagem é multifatorial
-   engajamento está associado ao desempenho
-   fatores psicossociais ajudam a explicar vulnerabilidade educacional
-   fases mais avançadas tendem a apresentar maior desenvolvimento
    educacional

------------------------------------------------------------------------

## 14. Como executar

Instalar dependências:

pip install -r requirements.txt

Executar o dashboard:

streamlit run app/Home.py

------------------------------------------------------------------------

## 15. Entregáveis do Tech Challenge

Este projeto inclui:

-   notebook de análise exploratória
-   notebook de modelagem
-   modelo treinado
-   dashboard interativo
-   documentação completa
-   roteiro de apresentação
-   vídeo explicativo

------------------------------------------------------------------------

## Autor

Diego Maradini\
FIAP --- Tech Challenge 5
