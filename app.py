import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import locale
import os
from datetime import datetime
import locale
locale.setlocale(locale.LC_ALL, "de_DE")

st.set_page_config(
                    page_title="Análise de Dados",
                    layout="wide", 
                    page_icon="cotralti_logo.png",
                    #initial_sidebar_state="collapsed" # inicia com barra de filtros fechada
)

with st.sidebar:
    st.title("Análise rápida spice")
    st.sidebar.markdown("""
                    #### Desenvolvido  por http://cotralti.com.br
                    """)
    uploader_file = st.file_uploader("Coloque o arraste o seu arquivo aqui.")
    
if uploader_file is not None:
    df = pd.read_excel(uploader_file)
    
    st.success("Conseguimos Carregar os seus dados :)")
    
    def corrigir_nomes(nome):
        nome = nome.replace('ARC-', '').replace('MILK RUN', '').replace('ARC-SZ01WR - WESTROCK', 'WESTROCK').replace('COT052 - AEROPORTO - SZ X VCP', 'Aeroporto VCP')
        return nome
    
    with st.sidebar:
        estado_destino = df["Estado Destino"].unique().tolist()
        df['Tabela de Preço'] = df["Tabela de Preço"].apply(corrigir_nomes)
        df["Coleta"] = pd.to_datetime(df["Coleta"])
        df["Mes"] = df["Coleta"].dt.month_name(locale.setlocale(locale.LC_ALL,'pt_BR.UTF-8'))
        
        with open ('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
    mes = st.sidebar.multiselect(
                        key=1,
                        label="Mes",
                        options=df["Mes"].unique(),
                        default=df["Mes"].unique()
                        )
    estado_destino= st.sidebar.multiselect(
                        key=2,
                        label="Estado Destino",
                        options=df["Estado Destino"].unique(),
                        default=df["Estado Destino"].unique()
                        )

    tabela_preco = st.sidebar.multiselect(
                        key=3,
                        label="Tabela de Preço",
                        options=df["Tabela de Preço"].unique(),
                        default=None
                        )
                    
    df = df.query("Mes == @mes and `Estado Destino` == @estado_destino and `Tabela de Preço` == @tabela_preco")

 
    st.header("Análise de Dados retirados do sistema.", divider='gray')
    
    # Criação de Cards
    
    def criar_card(icone, numero, texto , coluna_card):
        container = coluna_card.container(border=True)
        coluna_esquerda , coluna_direita = container.columns([1, 2.5])
        coluna_esquerda.image(f"imagens/{icone}")
        coluna_direita.write(numero)
        coluna_direita.write(texto)
        
    coluna_esquerda , coluna_meio , coluna_direita = st.columns([1, 1, 1])
    
    criar_card("Peso.png",f'{df["Peso Real"].sum():,.2f}',"Total de Peso (Toneladas)", coluna_esquerda)
    criar_card("notafiscal.png",f'{df["Nota Fiscal"].count():,}', "Total de Nota Fiscal (Und)", coluna_meio)
    criar_card("fretepeso.png",f' R$ {df["Frete Peso"].sum():,.2f}', "Total de Frete Peso (R$)", coluna_direita)
    
    criar_card("valortransportado.png",f'R$ {df["Valor N.F."].sum():,.2f}', "Valor Transportado (R$)", coluna_esquerda)
    criar_card("icms.png",f'R$ {df["Valor ICMS"].sum():,.2f}', "Valor Gasto com ICMS (R$)", coluna_meio)
    criar_card("seguro.png",f'R$ {df["ADValorem"].sum():,.2f}', "Valor do ADValorem (R$)", coluna_direita)

#Area do GRafico


base_mensal = df.groupby(df["Coleta"].dt.to_period("M")).sum(numeric_only=True).reset_index()
base_mensal["Coleta"] = base_mensal["Coleta"].dt.to_timestamp()

container = st.container(border=False)
with container:
    
        #grafico de area
        st.write("### Total de Frete Peso por Mês (R$)")
        grafico_area = px.area(base_mensal, x="Coleta", y="Frete Peso")
        st.plotly_chart(grafico_area)
           
colunas_aparecer = ["Número CT-e","Destinatário","Cidade Destinatário", "Tabela de Preço", "Nota Fiscal","Peso Real","Usuário cadastro", "Coleta"]
st.dataframe(df[colunas_aparecer],use_container_width=True,
                  column_config= { "Coleta": st.column_config.DateColumn("Data Faturamento",  format="DD.MM.YYYY",
            step=1,)
                      },hide_index=True)        
st.write("""
         &copy; 2024 - Luis Felipe A. David. Todos os direitos reservados
         """)