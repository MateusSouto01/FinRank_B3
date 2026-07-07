# Entrega do Projeto de Parceria Semantix

## Projeto: FinRank B3

**Repositório GitHub:**  
https://github.com/MateusSouto01/FinRank_B3

---

## 1. Resumo do projeto

O projeto **FinRank B3** é uma aplicação de Ciência de Dados voltada ao mercado financeiro brasileiro, com foco em fintechs, corretoras digitais e plataformas de investimento.

A proposta foi construir uma solução de apoio à decisão para priorização de ativos da B3, usando dados públicos, análise exploratória, engenharia de atributos financeiros e modelos de machine learning.

A ideia não foi criar um “robô mágico” que prevê preço de ação, mas sim uma camada analítica mais realista: um modelo capaz de apoiar a triagem e o ranking de ativos com base em risco, liquidez, retorno histórico e probabilidade de superar um benchmark em uma janela futura de 60 pregões.

---

## 2. Problema escolhido

Fintechs e corretoras precisam lidar com o desafio de oferecer produtos de investimento de forma personalizada e compatível com o perfil de risco dos clientes.

Nem todo ativo serve para todo investidor. Um papel pode ter retorno alto, mas também pode carregar volatilidade elevada, drawdown forte ou baixa liquidez.

Dessa forma, o problema central do projeto foi:

> Como identificar e priorizar ativos da B3 com maior probabilidade de superar um benchmark em 60 pregões, considerando também risco, liquidez e comportamento histórico?

---

## 3. Fontes de dados

Foram utilizados dados públicos e não confidenciais da B3, principalmente os arquivos históricos COTAHIST.

A base contém informações como:

- data do pregão;
- ticker;
- preço de abertura;
- preço máximo;
- preço mínimo;
- preço médio;
- preço de fechamento;
- número de negócios;
- quantidade negociada;
- volume negociado.

A base final usada na modelagem ficou com:

- 57.200 observações;
- 35 colunas;
- 35 ativos;
- período de 2019-01-11 até 2025-10-22.

---

## 4. Análise exploratória

Na análise exploratória foram avaliados os principais pontos relevantes para o problema:

- distribuição da variável alvo;
- ativos com maior frequência de superação do benchmark;
- retorno médio futuro por ativo;
- volatilidade média;
- liquidez média;
- drawdown;
- matriz de correlação;
- relação risco x retorno;
- classificação dos ativos por perfil de risco.

Um dos principais aprendizados foi que retorno sozinho não é suficiente para priorizar ativos. Alguns papéis apresentaram retorno médio elevado, mas também carregaram alto risco, forte drawdown e comportamento mais especulativo.

Por isso, o projeto combinou retorno, risco, liquidez e suitability para construir uma visão mais completa.

---

## 5. Modelagem

O problema foi tratado como uma tarefa de classificação binária.

A variável alvo foi:

`target_supera_benchmark_60d`

Onde:

- `1` = ativo superou o benchmark nos próximos 60 pregões;
- `0` = ativo não superou o benchmark nos próximos 60 pregões.

Foram testados três modelos:

- Regressão Logística;
- Árvore de Decisão;
- Random Forest.

A separação entre treino e teste foi feita de forma temporal, para respeitar a lógica do mercado financeiro: treinar com dados do passado e testar em dados mais recentes.

---

## 6. Resultados

| Modelo | Accuracy | Precision classe 1 | Recall classe 1 | F1 classe 1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Regressão Logística | 0.5903 | 0.5162 | 0.1365 | 0.2159 | 0.5425 |
| Árvore de Decisão | 0.5849 | 0.4973 | 0.3992 | 0.4429 | 0.5477 |
| Random Forest | 0.5841 | 0.4945 | 0.2899 | 0.3655 | 0.5422 |

O modelo principal escolhido foi a **Árvore de Decisão**, por apresentar o melhor equilíbrio entre recall, F1-score e ROC-AUC para a classe positiva.

A **Random Forest** foi usada como modelo auxiliar para análise de importância das variáveis e construção de ranking probabilístico de ativos.

As variáveis mais relevantes estiveram ligadas a:

- liquidez;
- volatilidade histórica;
- drawdown;
- retorno de médio/longo prazo;
- distância da máxima recente.

---

## 7. Visualizações

O projeto apresenta visualizações salvas no repositório, incluindo:

- distribuição da variável alvo;
- mapa de risco x retorno;
- matriz de correlação;
- comparação de desempenho dos modelos;
- matriz de confusão;
- importância das variáveis;
- ranking de ativos por probabilidade;
- taxa real de superação por faixa de probabilidade.

Essas visualizações estão disponíveis na pasta `images/` do repositório.

---

## 8. Conclusão

O projeto mostrou que é possível usar dados públicos da B3 para construir uma solução analítica voltada ao contexto de fintechs e corretoras digitais.

Os resultados indicam que existe algum sinal preditivo nas variáveis criadas, especialmente em métricas ligadas a liquidez, volatilidade, drawdown e retornos acumulados.

Ao mesmo tempo, o projeto reconhece que prever superação de benchmark no mercado financeiro é uma tarefa difícil e ruidosa. Por isso, a solução não deve ser interpretada como recomendação automática de compra ou venda.

A melhor leitura é:

> O modelo funciona como uma camada de apoio à decisão, ajudando a priorizar ativos para análise, combinar filtros de risco e liquidez, e apoiar uma lógica de suitability em uma fintech.

---

## 9. Tecnologias utilizadas

- Python;
- Pandas;
- NumPy;
- Matplotlib;
- Scikit-learn;
- Jupyter Notebook;
- Git;
- GitHub.

---

## 10. Observação

Este projeto tem finalidade educacional e analítica.  
Não representa recomendação de investimento, compra ou venda de ativos.

O objetivo é demonstrar aplicação de Ciência de Dados em um problema realista de mercado financeiro, com uso de dados públicos, análise exploratória, modelagem supervisionada e interpretação dos resultados.