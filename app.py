import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import locale

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
    
    def formatar(valor):
        return "{:,.2f}".format(valor)
    
    
    with st.sidebar:
        estado_destino = df["Estado Destino"].unique().tolist()
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

    df = df.query("Mes == @mes and `Estado Destino` == @estado_destino")

 
    st.header("Análise de Dados retirados do sistema.", divider='gray')
    
    total_peso = f"{round(df["Peso Real"].sum(),2):,.0f}"
    total_nf = f"{len(df['Nota Fiscal'].value_counts()):,.0f}"
    valor_tranportado = f"{round(df['Valor N.F.'].sum(),2):,.0f}"
    total_frete_peso =f" R$ {round(df['Frete Peso'].sum(),2):,.0f}"
    
    col1,col2,col3, col4 = st.columns(4)
                #col1.metric("Total de Peso", total_peso)
    col1.metric(label="Total de Peso Carregado", value=total_peso)
    col2.metric("Total de Nota Fiscal", value=total_nf)
    col3.metric("Total de Frete Peso", total_frete_peso)
    col4.metric("Total de valor transportado", valor_tranportado)
    
    colunas_aparecer = ["Número CT-e","Destinatário","Cidade Destinatário", "Tabela de Preço", "Nota Fiscal","Peso Real","Usuário cadastro", "Coleta"]
    st.dataframe(df[colunas_aparecer],use_container_width=True,
                  column_config= { "Coleta": st.column_config.DateColumn("Data Faturamento",  format="DD.MM.YYYY",
            step=1,)
                      },hide_index=True)
    
    fig = px.bar(df, x=df["Mes"], y=df["Frete Peso"], title="Faturamento Mensal",color=df["Estado Destino"])
    
    st.plotly_chart(fig)

    st.write("""
         &copy; 2024 - Luis Felipe A. David. Todos os direitos reservados
         """)
