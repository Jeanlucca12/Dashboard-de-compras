from datetime import datetime
from unicodedata import decimal
import pandas as pd
import streamlit as st

caminho_datasets = "datasets"

df_compras = pd.read_csv(f"{caminho_datasets}/compras.csv", decimal=",", sep=";", index_col=0)
df_lojas = pd.read_csv(f"{caminho_datasets}/lojas.csv", decimal=",", sep=";")
df_produtos = pd.read_csv(f"{caminho_datasets}/produtos.csv", decimal=",", sep=";")

df_lojas["cidade/estado"] = df_lojas["cidade"] + "/" + df_lojas["estado"]
lista_lojas = df_lojas["cidade/estado"].to_list()
loja_selecionada = st.sidebar.selectbox("Selecione a loja:", lista_lojas)

lista_vendedores = df_lojas.loc[df_lojas["cidade/estado"] == loja_selecionada, "vendedores"].iloc[0]
lista_vendedores = lista_vendedores.strip("][").replace("'", "").split(", ")
vendedor_selecionado = st.sidebar.selectbox("Selecione o vendedor:", lista_vendedores)

lista_produtos = df_produtos["nome"].to_list()
produto_selecionado = st.sidebar.selectbox("Selecione o produto:", lista_produtos)

nome_cliente = st.sidebar.text_input("Nome do cliente:")
genero_selecionado = st.sidebar.selectbox("Gênero do cliente:", ["Masculino", "Feminino"])

forma_pagto_selecionada = st.sidebar.selectbox("Forma de pagamento:", ["cartão de crédito", "Boleto", "Pix", "Dinheiro"])

if st.sidebar.button("Adicionar Nova Compra"):

    lista_adicionar = [
        df_compras["id_compra"].max() + 1 if not df_compras.empty else 1,
        loja_selecionada,
        vendedor_selecionado,
        produto_selecionado,
        nome_cliente,
        genero_selecionado,
        forma_pagto_selecionada
    ]

    df_compras.loc[datetime.now()] = lista_adicionar

    df_compras.to_csv(
        f"{caminho_datasets}/compras.csv",
        index=False,
        decimal=",",
        sep=";"
    )

    st.success("Nova compra adicionada com sucesso!")

st.dataframe(df_compras)