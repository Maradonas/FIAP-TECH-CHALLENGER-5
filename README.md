# FIAP Tech Challenge 5 — Dashboard Analítico e Preditivo | Passos Mágicos

## Visão geral

Este projeto foi desenvolvido para o **FIAP Tech Challenge 5**, com base no case **Passos Mágicos**.  
O objetivo é construir uma solução de análise de dados e predição de risco de defasagem escolar, transformando os indicadores educacionais em um **dashboard interativo em Streamlit**.

A aplicação foi estruturada para responder de forma visual e executiva às principais perguntas do case, com foco em:

- desempenho acadêmico
- defasagem escolar
- engajamento
- autoavaliação
- fatores psicossociais e psicopedagógicos
- risco de defasagem
- indícios de efetividade do programa ao longo do tempo

---

## Objetivo do projeto

O projeto possui dois grandes blocos:

### 1. Análise Exploratória
Investigar o comportamento dos indicadores da base para entender padrões, relações e sinais relevantes para o case.

### 2. Modelo Preditivo
Treinar um modelo de machine learning capaz de estimar a probabilidade de um aluno estar em **risco de defasagem**, com base nos indicadores disponíveis.

---

## Estrutura do projeto

```bash
FIAP-TECH-CHALLENGER-5/
│
├── app/
│   ├── Home.py
│   ├── pages/
│   │   ├── 1_Modelo.py
│   │   └── 2_Analise_Exploratoria.py
│   └── utils/
│       ├── loaders.py
│       └── charts.py
│
├── data/
│   ├── BASE DE DADOS PEDE 2024 - DATATHON.xlsx
│   └── processed/
│       ├── base_unificada.csv
│       └── diagnostico_base.json
│
├── models/
│   ├── modelo_risco_defasagem.joblib
│   └── metricas_modelo.json
│
├── notebooks/
├── src/
├── 01_EDA_Passos_Magicos_chumbado.py
├── 02_Modelo_Risco_Defasagem_chumbado.py
└── README.md
```

---

## Explicação dos principais arquivos

### `app/Home.py`
Página inicial do dashboard.

Responsabilidades:
- apresentar o projeto
- exibir resumo executivo
- mostrar conclusões gerais da análise
- orientar a navegação entre as páginas

---

### `app/pages/1_Modelo.py`
Página do modelo preditivo.

Responsabilidades:
- exibir métricas do modelo
- mostrar importância das variáveis
- disponibilizar simulador de risco
- calcular a probabilidade de risco de defasagem com base nas features do modelo salvo

---

### `app/pages/2_Analise_Exploratoria.py`
Página de análise exploratória.

Responsabilidades:
- exibir gráficos analíticos
- permitir filtro por ano
- responder visualmente às perguntas do case
- apresentar interpretações executivas abaixo de cada gráfico

---

### `app/utils/loaders.py`
Camada de carregamento e padronização de dados e modelo.

Responsabilidades:
- carregar a base tratada
- carregar o modelo salvo
- carregar métricas do modelo
- normalizar colunas
- reconstruir variáveis importantes como `inde`, `pedra`, `faixa_ian` e `risco_defasagem`
- montar corretamente a entrada do simulador com as features esperadas pelo modelo

---

### `app/utils/charts.py`
Camada responsável pela geração dos gráficos.

Responsabilidades:
- criar visualizações padronizadas
- centralizar estilo visual
- evitar dependências desnecessárias
- manter consistência entre gráficos do dashboard

---

### `01_EDA_Passos_Magicos_chumbado.py`
Script de preparação da base.

Responsabilidades:
- ler o Excel bruto
- consolidar as abas anuais
- padronizar colunas
- corrigir tipos
- reconstruir colunas relevantes
- gerar `base_unificada.csv`
- gerar `diagnostico_base.json`

---

### `02_Modelo_Risco_Defasagem_chumbado.py`
Script de treino do modelo.

Responsabilidades:
- ler a base tratada
- selecionar features
- treinar o modelo
- avaliar desempenho
- salvar o pipeline treinado em `.joblib`
- salvar métricas em `.json`

---

## Dados utilizados

A base do projeto é derivada do arquivo Excel do case, consolidando diferentes anos do programa.  
Durante o tratamento, foram considerados indicadores como:

- `IDA` — Indicador de desempenho acadêmico
- `IEG` — Indicador de engajamento
- `IAA` — Indicador de autoavaliação
- `IPS` — Indicador psicossocial
- `IPP` — Indicador psicopedagógico
- `IAN` — Indicador de adequação de nível
- `INDE` — Indicador geral de desenvolvimento
- `PEDRA` / `FASE` — classificação/fase do aluno no programa

---

## Regra de risco de defasagem

Um dos pontos mais importantes do projeto foi corrigir a lógica do alvo (`target`) de classificação.

### Problema encontrado
Uma regra simplificada baseada apenas em `IAN >= 1` gerava distorções graves, como:
- 100% dos alunos classificados como risco
- distribuição inconsistente das faixas de IAN
- perda de credibilidade dos gráficos e do modelo

### Regra adotada
A lógica priorizada foi:

```python
risco_defasagem = 1 se defasagem < 0
```

Fallbacks:
- se `defasagem` não existir, usar `defas < 0`
- apenas em último caso, usar uma aproximação com `ian <= 5`

Essa abordagem torna a variável-alvo mais coerente com a ideia de atraso em relação à fase ideal.

---

## Classificação de IAN

Na base do case, o `IAN` aparece majoritariamente com valores como:

- `2.5`
- `5.0`
- `10.0`

Por isso, a classificação foi ajustada para refletir a escala real dos dados:

- `<= 2.5` → **Severa**
- `<= 5` → **Moderada**
- `< 10` → **Leve**
- `>= 10` → **Adequada**

Isso evita o erro de concentrar tudo em uma única categoria.

---

## Modelo utilizado

A solução atual usa um modelo supervisionado para prever risco de defasagem.

### Features utilizadas na versão estável
- `ida`
- `ieg`
- `ips`
- `ipp`
- `iaa`

Essas features foram escolhidas para manter consistência entre:
- treino
- métricas salvas
- inferência no dashboard

Isso também eliminou inconsistências como:
- `ipv` vs `ianv`
- colunas diferentes entre treinamento e simulador

---

## Como executar o projeto

### 1. Preparar a base tratada
```bash
python .\01_EDA_Passos_Magicos_chumbado.py
```

### 2. Treinar o modelo
```bash
python .\02_Modelo_Risco_Defasagem_chumbado.py
```

### 3. Executar o dashboard
```bash
streamlit run .\app\Home.py
```

---

## Funcionalidades do dashboard

### Home
- resumo executivo
- conclusões do projeto
- contextualização geral

### Modelo
- métricas do modelo
- importância das variáveis
- simulador de risco
- probabilidade predita

### Análise Exploratória
- filtro por ano
- perfil de defasagem
- evolução do desempenho
- análise de relações entre indicadores
- comparação por risco
- análise por fase
- heatmap de correlação
- leitura executiva dos resultados

---

## Principais decisões técnicas

### 1. Remoção da dependência de `statsmodels`
O uso de `trendline="ols"` no Plotly gerava erro por depender de `statsmodels`.  
A solução adotada foi substituir isso por uma linha de tendência calculada diretamente, evitando dependência desnecessária.

### 2. Padronização dos nomes de colunas
As colunas foram normalizadas para evitar problemas com:
- acentos
- espaços
- variações entre anos
- nomes divergentes entre base e modelo

### 3. Alinhamento entre treino e inferência
O simulador do Streamlit foi ajustado para usar exatamente as mesmas features do modelo salvo, na mesma ordem esperada pelo pipeline.

### 4. Foco em apresentação executiva
Os gráficos foram organizados com storytelling e interpretação textual, visando facilitar a defesa do projeto perante a banca.

---

## Limitações atuais

Apesar de a solução estar funcional e coerente, ainda existem pontos que podem ser melhorados:

- o modelo ainda pode evoluir em poder preditivo
- a base pode conter limitações estruturais e ausência de algumas variáveis
- a definição de risco depende da qualidade da variável `defasagem`
- a interpretação de efetividade do programa ainda é exploratória e não causal

---

## Próximos passos sugeridos

### 1. Melhorar a acurácia do modelo
Este é um dos próximos passos mais importantes.

Possibilidades:
- testar novos algoritmos
- fazer tuning de hiperparâmetros
- balancear classes, se necessário
- avaliar feature engineering
- comparar modelos com validação cruzada
- incluir novas variáveis relevantes, desde que estejam consistentes entre treino e inferência

### 2. Refinar a engenharia de atributos
Sugestões:
- criar interações entre indicadores
- testar versões normalizadas
- construir indicadores compostos
- explorar segmentações por fase e ano

### 3. Melhorar a robustez da definição de risco
Hoje o target está mais coerente, mas ainda pode ser refinado com apoio do entendimento pedagógico do case.

### 4. Fortalecer a explicação de efetividade do programa
A próxima evolução pode incluir:
- análise longitudinal mais forte
- coortes por fase
- comparação entre grupos ao longo dos anos
- métricas mais específicas de progresso

### 5. Evoluir a camada visual
Sugestões:
- cards mais sofisticados
- identidade visual mais forte
- destaques automáticos de insights
- seção final com recomendações executivas

### 6. Criar pipeline reprodutível de ponta a ponta
Uma evolução importante seria transformar todo o fluxo em pipeline único:
- ingestão
- tratamento
- treino
- avaliação
- atualização automática do dashboard

---

## Conclusão

Este projeto busca transformar os dados do case Passos Mágicos em uma solução analítica e preditiva consistente, visualmente clara e aderente ao contexto do desafio.

A entrega combina:
- tratamento de dados
- análise exploratória
- modelagem preditiva
- visualização interativa
- foco em comunicação executiva

O resultado final não é apenas um painel, mas uma base sólida para discutir:
- desempenho dos alunos
- fatores associados à defasagem
- risco futuro
- sinais de efetividade do programa

---

## Autor

**Diego Maradini**  
Projeto desenvolvido para o **FIAP Tech Challenge 5**.
