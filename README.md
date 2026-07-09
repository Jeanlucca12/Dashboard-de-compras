# 📊 Dashboard de Compras — Análise de Vendas com Python, Pandas e Streamlit

Dashboard interativo para análise de dados de vendas de uma rede fictícia de lojas, construído com **Python**, **Pandas** e **Streamlit**. O projeto simula um cenário real de análise de dados: geração de uma base de dados sintética, tratamento com Pandas e visualização interativa em uma aplicação web com múltiplas abas.

## 🎯 O que este projeto demonstra

- **Geração e manipulação de dados** com Pandas (leitura/escrita de CSV e Excel, merges, índices de data, colunas calculadas)
- **Construção de dashboards web** com Streamlit (múltiplas abas, filtros, formulários, métricas)
- **Tabelas dinâmicas (pivot tables)** configuráveis pelo usuário — índices, colunas e métricas de agregação são escolhidos em tempo real na interface
- **KPIs de negócio**: valor total de vendas, quantidade de compras, loja com melhor desempenho, vendedor com maior faturamento e cálculo de comissão
- **CRUD simples**: cadastro de novas compras diretamente pela interface, persistido no CSV

- ## Veja ele no ar utilizando o Streamlit Cloud!
- Link: https://dashboard-de-compras-analytics.streamlit.app/

## 🗂️ Estrutura do projeto

```
Dashboard-de-compras/
├── app.py              # Aplicação única, com uma aba para cada funcionalidade
├── requirements.txt     # Dependências do projeto
└── datasets/            # CSVs/Excel gerados (compras, lojas, produtos)
```

Todo o dashboard roda a partir de um único arquivo, **`app.py`**, organizado em 5 abas — cada uma representando uma etapa do aprendizado original do projeto:

| Aba | O que faz |
|---|---|
| 📄 **Visão Geral** | Exibe a base completa de compras, sem tratamento |
| 🔍 **Filtrar Colunas** | Seleciona colunas específicas e filtra por coluna/valor |
| ➕ **Nova Compra** | Formulário para cadastrar uma nova compra (loja, vendedor, produto, cliente, pagamento) e salvar no CSV |
| 📈 **Indicadores** | KPIs por período: valor total vendido, quantidade de compras, loja e vendedor principais, comissão |
| 🧮 **Tabela Dinâmica** | Pivot table interativa, com índices, colunas e métrica (soma/contagem) escolhidos pelo usuário |

Na barra lateral também é possível **gerar um novo dataset de exemplo** com um clique, sem precisar rodar nenhum script separado — útil para quem for testar o projeto pela primeira vez.

## 🛠️ Tecnologias

- **Python 3**
- **Pandas** — tratamento e agregação de dados
- **Streamlit** — construção da interface web interativa
- **names** — geração de nomes fictícios para os dados sintéticos
- **openpyxl** — exportação dos dados também em formato Excel

## 🚀 Como rodar localmente

```bash
# Clone o repositório
git clone https://github.com/Jeanlucca12/Dashboard-de-compras.git
cd Dashboard-de-compras

# Instale as dependências
pip install -r requirements.txt

# Rode o dashboard
streamlit run app.py
```

Na primeira execução, se ainda não existir uma base de dados, o app avisa e basta clicar em **"🔄 Gerar novo dataset de exemplo"** na barra lateral para criar os dados fictícios automaticamente.

## 📈 Principais funcionalidades do dashboard

- **Filtro por período**: seleção de data inicial e final para análise de indicadores
- **Métricas em tempo real**: valor total e quantidade de compras no período
- **Ranking automático**: loja e vendedor com melhor performance no período selecionado
- **Cálculo de comissão**: 5% sobre o valor vendido por vendedor
- **Cadastro de novas compras** direto pela interface, sem precisar editar o CSV manualmente
- **Tabela dinâmica configurável**: o usuário escolhe quais colunas viram índice, quais viram cabeçalho e qual métrica deseja visualizar


## 💡 Próximos passos (ideias de evolução)

- Adicionar gráficos (linha, barras) com Plotly ou Altair
- Adicionar testes automatizados para as funções de tratamento de dados
- Deploy no Streamlit Community Cloud para demonstração ao vivo

---

Desenvolvido por [Jeanlucca12](https://github.com/Jeanlucca12) como parte de um portfólio de análise de dados.
