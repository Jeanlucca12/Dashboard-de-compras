"""
Dashboard de Compras
--------------------
App único (Streamlit) que reúne, em forma de abas, os 5 estudos que compõem
este projeto de análise de dados: visualização de tabela, seleção/filtro de
colunas, cadastro de novas compras, indicadores de vendas (KPIs) e uma
tabela dinâmica (pivot table) configurável pelo usuário.

Para rodar: streamlit run app.py
"""

import random
from datetime import datetime, timedelta
from pathlib import Path

import names
import pandas as pd
import streamlit as st

# ============================================================
# CONFIGURAÇÕES E CONSTANTES GERAIS
# ============================================================
st.set_page_config(page_title="Dashboard de Compras", page_icon="🛒", layout="wide")

CAMINHO_DATASETS = "datasets"
PERC_COMISSAO = 0.05

# Colunas usadas como possíveis índices/colunas da tabela dinâmica (aba 5)
COLUNAS_ANALISE = ["loja", "vendedor", "produto", "cliente_genero", "forma_pagamento"]
COLUNAS_NUMERICAS = ["preco", "comissao"]
FUNCOES_AGREGACAO = {"soma": "sum", "contagem": "count"}

# Dados de referência usados para gerar um dataset de exemplo do zero
LOJAS_BASE = [
    {"estado": "SP", "cidade": "São Paulo", "vendedores": ["Ana Oliveira", "Lucas Pereira"]},
    {"estado": "MG", "cidade": "Belo Horizonte", "vendedores": ["Carlos Silva", "Fernanda Costa"]},
    {"estado": "RJ", "cidade": "Rio de Janeiro", "vendedores": ["Juliana Almeida", "Pedro Souza"]},
    {"estado": "RS", "cidade": "Porto Alegre", "vendedores": ["Mariana Gomes", "Roberto Ferreira"]},
    {"estado": "SC", "cidade": "Florianópolis", "vendedores": ["Gabriela Santos", "Tiago Lima"]},
]

PRODUTOS_BASE = [
    {"nome": "Smartphone Samsung Galaxy", "id": 0, "preco": 2500},
    {"nome": "Notebook Dell Inspiron", "id": 1, "preco": 4500},
    {"nome": "Tablet Apple Ipad", "id": 2, "preco": 3000},
    {"nome": "Smartwatch Garmin", "id": 3, "preco": 1200},
    {"nome": "Fone de Ouvido Sony", "id": 4, "preco": 600},
]

FORMAS_PAGAMENTO_BASE = ["cartão de crédito", "boleto", "pix", "dinheiro"]
GENEROS_BASE = ["male", "female"]


# ============================================================
# FUNÇÕES DE APOIO (usadas por mais de uma aba)
# ============================================================
def gerar_dataset(qtd_compras: int = 2000):
    """
    Cria uma base de dados fictícia (compras, lojas e produtos) e salva em
    datasets/*.csv e *.xlsx. Útil para testar o dashboard sem precisar de
    uma base de dados real. Equivale ao antigo script `gera_dataset.py`.
    """
    pasta_datasets = Path(CAMINHO_DATASETS)
    pasta_datasets.mkdir(parents=True, exist_ok=True)

    compras = []
    for _ in range(qtd_compras):
        loja = random.choice(LOJAS_BASE)
        vendedor = random.choice(loja["vendedores"])
        produto = random.choice(PRODUTOS_BASE)
        hora_compra = datetime.now() - timedelta(
            days=random.randint(1, 365),
            hours=random.randint(-5, 5),
            minutes=random.randint(-30, 30),
        )
        genero_cliente = random.choice(GENEROS_BASE)
        nome_cliente = names.get_full_name(genero_cliente)
        forma_pagto = random.choice(FORMAS_PAGAMENTO_BASE)

        compras.append({
            "data": hora_compra,
            "id_compra": 0,
            "loja": loja["cidade"],
            "vendedor": vendedor,
            "produto": produto["nome"],
            "cliente_nome": nome_cliente,
            "cliente_genero": genero_cliente.replace("female", "feminino").replace("male", "masculino"),
            "forma_pagamento": forma_pagto,
        })

    df_compras = pd.DataFrame(compras).set_index("data").sort_index()
    df_compras["id_compra"] = list(range(len(df_compras)))

    df_lojas = pd.DataFrame(LOJAS_BASE)
    df_produtos = pd.DataFrame(PRODUTOS_BASE)

    df_compras.to_csv(pasta_datasets / "compras.csv", decimal=",", sep=";")
    df_lojas.to_csv(pasta_datasets / "lojas.csv", decimal=",", sep=";")
    df_produtos.to_csv(pasta_datasets / "produtos.csv", decimal=",", sep=";")

    df_compras.to_excel(pasta_datasets / "compras.xlsx")
    df_lojas.to_excel(pasta_datasets / "lojas.xlsx")
    df_produtos.to_excel(pasta_datasets / "produtos.xlsx")


def carregar_dados():
    """
    Lê os três CSVs que sustentam o dashboard (compras, lojas e produtos)
    e devolve os três DataFrames sem nenhuma transformação. Mantida
    separada de `adicionar_preco_e_comissao` para que cada aba só faça o
    tratamento de dados que realmente precisa.
    """
    df_compras = pd.read_csv(
        f"{CAMINHO_DATASETS}/compras.csv", decimal=",", sep=";", index_col=0, parse_dates=True
    )
    df_lojas = pd.read_csv(f"{CAMINHO_DATASETS}/lojas.csv", decimal=",", sep=";", index_col=0)
    df_produtos = pd.read_csv(f"{CAMINHO_DATASETS}/produtos.csv", decimal=",", sep=";", index_col=0)
    return df_compras, df_lojas, df_produtos


def adicionar_preco_e_comissao(df_compras, df_produtos):
    """
    Junta (merge) o preço de cada produto na tabela de compras e calcula a
    comissão do vendedor (5% do valor vendido). Usada pelas abas de
    Indicadores e Tabela Dinâmica, que precisam de valores em R$.
    """
    df_produtos = df_produtos.rename(columns={"nome": "produto"})
    df = df_compras.reset_index()
    df = pd.merge(df, df_produtos[["produto", "preco"]], on="produto", how="left")
    df = df.set_index("data")
    df["comissao"] = df["preco"] * PERC_COMISSAO
    return df


def dataset_existe() -> bool:
    """Verifica se o dataset de compras já foi gerado ao menos uma vez."""
    return (Path(CAMINHO_DATASETS) / "compras.csv").exists()


# ============================================================
# BARRA LATERAL — geração do dataset de exemplo
# ============================================================
st.sidebar.header("⚙️ Base de dados")
st.sidebar.caption("Gere uma base fictícia de compras para testar o dashboard.")
if st.sidebar.button("🔄 Gerar novo dataset de exemplo"):
    gerar_dataset()
    st.sidebar.success("Dataset gerado em datasets/!")

if not dataset_existe():
    st.warning(
        "Nenhum dataset encontrado. Clique em **'Gerar novo dataset de exemplo'** "
        "na barra lateral para criar dados fictícios e explorar o dashboard."
    )
    st.stop()


# ============================================================
# CABEÇALHO E ABAS
# ============================================================
st.title("🛒 Dashboard de Compras")
st.caption("Análise de vendas de uma rede fictícia de lojas — Python, Pandas e Streamlit")

aba_visao_geral, aba_filtro, aba_nova_compra, aba_indicadores, aba_tabela_dinamica = st.tabs(
    ["📄 Visão Geral", "🔍 Filtrar Colunas", "➕ Nova Compra", "📈 Indicadores", "🧮 Tabela Dinâmica"]
)

# ------------------------------------------------------------
# ABA 1 — Visão Geral (equivalente a 1-visualizando_tb.py)
# Mostra a base de compras completa, sem nenhum tratamento.
# ------------------------------------------------------------
with aba_visao_geral:
    st.subheader("Base completa de compras")
    df_compras, _, _ = carregar_dados()
    st.dataframe(df_compras, use_container_width=True)

# ------------------------------------------------------------
# ABA 2 — Filtrar Colunas (equivalente a 2-selecionando_colunas.py)
# Permite escolher quais colunas exibir e filtrar por um valor específico.
# ------------------------------------------------------------
with aba_filtro:
    st.subheader("Filtrar e selecionar colunas")
    df_compras, _, _ = carregar_dados()

    colunas = list(df_compras.columns)
    colunas_selecionadas = st.multiselect(
        "Selecione as colunas:", colunas, default=colunas, key="colunas_tab2"
    )

    col1, col2 = st.columns(2)
    col_filtro = col1.selectbox(
        "Selecione a coluna:", [c for c in colunas if c != "id_compra"], key="col_filtro_tab2"
    )
    valor_filtro = col2.selectbox(
        "Selecione o valor:", list(df_compras[col_filtro].unique()), key="valor_filtro_tab2"
    )

    botao_col1, botao_col2 = st.columns(2)
    filtrar = botao_col1.button("Filtrar", key="btn_filtrar_tab2")
    limpar = botao_col2.button("Limpar Filtro", key="btn_limpar_tab2")

    if filtrar:
        st.dataframe(
            df_compras.loc[df_compras[col_filtro] == valor_filtro, colunas_selecionadas],
            use_container_width=True,
        )
    else:
        # Também cobre o clique em "Limpar Filtro" e o estado inicial da aba
        st.dataframe(df_compras[colunas_selecionadas], use_container_width=True)

# ------------------------------------------------------------
# ABA 3 — Nova Compra (equivalente a 3-adicionando_linhas.py)
# Formulário para cadastrar uma nova compra e salvá-la no CSV.
# ------------------------------------------------------------
with aba_nova_compra:
    st.subheader("Cadastrar uma nova compra")
    df_compras, df_lojas, df_produtos = carregar_dados()

    df_lojas["cidade/estado"] = df_lojas["cidade"] + "/" + df_lojas["estado"]
    lista_lojas = df_lojas["cidade/estado"].to_list()

    col1, col2 = st.columns(2)
    loja_selecionada = col1.selectbox("Selecione a loja:", lista_lojas, key="loja_tab3")

    # A coluna "vendedores" é salva como texto de lista (ex: "['Ana', 'Lucas']"),
    # então precisamos "desmontar" essa string manualmente para virar uma lista de verdade.
    lista_vendedores = df_lojas.loc[df_lojas["cidade/estado"] == loja_selecionada, "vendedores"].iloc[0]
    lista_vendedores = lista_vendedores.strip("][").replace("'", "").split(", ")
    vendedor_selecionado = col2.selectbox("Selecione o vendedor:", lista_vendedores, key="vendedor_tab3")

    lista_produtos = df_produtos["nome"].to_list()
    produto_selecionado = col1.selectbox("Selecione o produto:", lista_produtos, key="produto_tab3")
    nome_cliente = col2.text_input("Nome do cliente:", key="cliente_tab3")

    col3, col4 = st.columns(2)
    genero_selecionado = col3.selectbox("Gênero do cliente:", ["Masculino", "Feminino"], key="genero_tab3")
    forma_pagto_selecionada = col4.selectbox(
        "Forma de pagamento:", ["cartão de crédito", "Boleto", "Pix", "Dinheiro"], key="pagto_tab3"
    )

    if st.button("Adicionar Nova Compra", key="btn_add_tab3"):
        nova_compra = [
            df_compras["id_compra"].max() + 1 if not df_compras.empty else 1,
            loja_selecionada,
            vendedor_selecionado,
            produto_selecionado,
            nome_cliente,
            genero_selecionado,
            forma_pagto_selecionada,
        ]

        # A data/hora atual vira o índice da nova linha, assim como no restante da base
        df_compras.loc[datetime.now()] = nova_compra

        # Observação: aqui usamos index=True (padrão) para manter a data como índice
        # ao salvar — no script original esse parâmetro estava como False, o que fazia
        # a coluna de data se perder no próximo carregamento. Foi ajustado nesta unificação.
        df_compras.to_csv(f"{CAMINHO_DATASETS}/compras.csv", decimal=",", sep=";")

        st.success("Nova compra adicionada com sucesso!")

    st.divider()
    st.dataframe(df_compras, use_container_width=True)

# ------------------------------------------------------------
# ABA 4 — Indicadores (equivalente a 4-volume_dados.py)
# KPIs de vendas por período: valor total, loja e vendedor principais.
# ------------------------------------------------------------
with aba_indicadores:
    st.subheader("Indicadores do período")
    df_compras, _, df_produtos = carregar_dados()
    df_compras = adicionar_preco_e_comissao(df_compras, df_produtos)

    data_default = df_compras.index.max()
    col1, col2 = st.columns(2)
    data_inicio = col1.date_input("Data inicial", value=data_default - timedelta(days=6), key="data_inicio_tab4")
    data_final = col2.date_input("Data final", value=data_default, key="data_final_tab4")

    # Filtra as compras dentro do intervalo de datas escolhido
    df_filtrado = df_compras[
        (df_compras.index.date >= data_inicio) & (df_compras.index.date < data_final + timedelta(days=1))
    ]

    st.markdown("### Números Gerais")
    col1, col2 = st.columns(2)
    valor_compras = df_filtrado["preco"].sum()
    col1.metric("Valor de compras no período", f"R$ {valor_compras:.2f}")
    col2.metric("Quantidade de compras no período", df_filtrado["preco"].count())

    st.divider()

    if not df_filtrado.empty:
        # Loja com maior número de compras no período
        principal_loja = df_filtrado["loja"].value_counts().idxmax()
        st.markdown(f"### Loja Principal: {principal_loja}")

        col1, col2 = st.columns(2)
        valor_loja = df_filtrado.loc[df_filtrado["loja"] == principal_loja, "preco"].sum()
        qtd_loja = df_filtrado.loc[df_filtrado["loja"] == principal_loja, "preco"].count()
        col1.metric("Valor vendido", f"R$ {valor_loja:.2f}")
        col2.metric("Quantidade de compras", qtd_loja)

        st.divider()

        # Vendedor com maior número de compras no período
        principal_vendedor = df_filtrado["vendedor"].value_counts().index[0]
        st.markdown(f"### Vendedor Principal: {principal_vendedor}")

        valor_vendedor = df_filtrado[df_filtrado["vendedor"] == principal_vendedor]["preco"].sum()
        comissao_vendedor = df_filtrado[df_filtrado["vendedor"] == principal_vendedor]["comissao"].sum()

        col1, col2 = st.columns(2)
        col1.metric("Valor das compras no período", f"R$ {valor_vendedor:.2f}")
        col2.metric("Comissão do vendedor no período", f"R$ {comissao_vendedor:.2f}")
    else:
        # Movido para dentro deste bloco: no script original, o cálculo do vendedor
        # principal rodava mesmo sem compras no período e quebrava o app.
        st.warning("Nenhuma compra encontrada para o período selecionado.")

# ------------------------------------------------------------
# ABA 5 — Tabela Dinâmica (equivalente a 5-tb_dinamica.py)
# Pivot table configurável: o usuário escolhe índices, colunas e métrica.
# ------------------------------------------------------------
with aba_tabela_dinamica:
    st.subheader("Tabela Dinâmica (Pivot Table)")
    df_compras, _, df_produtos = carregar_dados()
    df_compras = adicionar_preco_e_comissao(df_compras, df_produtos)

    col1, col2 = st.columns(2)
    indice_dinamico = col1.multiselect("Selecione os índices", COLUNAS_ANALISE, key="indice_tab5")
    colunas_disponiveis = [c for c in COLUNAS_ANALISE if c not in indice_dinamico]
    coluna_dinamica = col2.multiselect("Selecione as colunas", colunas_disponiveis, key="coluna_tab5")

    col3, col4 = st.columns(2)
    valor_analise = col3.selectbox("Selecione o valor", COLUNAS_NUMERICAS, key="valor_tab5")
    metrica_analise = col4.selectbox("Selecione a métrica", list(FUNCOES_AGREGACAO.keys()), key="metrica_tab5")

    if len(indice_dinamico) > 0 and len(coluna_dinamica) > 0:
        metrica = FUNCOES_AGREGACAO[metrica_analise]
        tabela_dinamica = pd.pivot_table(
            df_compras,
            index=indice_dinamico,
            columns=coluna_dinamica,
            values=valor_analise,
            aggfunc=metrica,
        )
        # Adiciona uma linha e uma coluna de totais gerais
        tabela_dinamica["TOTAL_GERAL"] = tabela_dinamica.sum(axis=1)
        tabela_dinamica.loc["TOTAL_GERAL"] = tabela_dinamica.sum(axis=0).to_list()

        st.dataframe(tabela_dinamica, use_container_width=True)
    else:
        st.info("Selecione ao menos um índice e uma coluna para gerar a tabela.")
