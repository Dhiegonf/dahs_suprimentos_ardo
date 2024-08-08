import streamlit as st
import pandas as pd
import datetime
from streamlit_dynamic_filters import DynamicFilters
import datetime

# leitura dos dfs e outra informações úteis
df_itens_compras = pd.read_pickle('itens_compras.pkl')
df_solicitacoes_compras = pd.read_pickle('solicitacoes_compras.pkl')


# streamlit run .\app_v1_sup_ardo.py
st.set_page_config(layout='wide')
st.title('Suprimentos')

aba1, aba2 = st.tabs(['Solicitações', 'Em produção'])

with aba1:
    
    st.subheader("Situação da solicitação de compras", divider="gray")
    num_solic = st.number_input("", value=None, placeholder="Informe o número de solicitação...")
    col1, col2, col3, col4 = st.columns(4)
    
    if num_solic == None:
        col1.metric("Data de criação da solicitação de compra", 0)
        col2.metric("Data da solicitação", 0)
        col3.metric("Status solicitação de compra", 0, "0 dias")
        col4.metric("Código da obra da solicitação", 0)

    elif ((df_solicitacoes_compras[df_solicitacoes_compras['id'].isin([num_solic])])['createdAt']).tolist() == []:
            st.error('Número de solicitação não encontrado', icon=None)

    else:
        
        x1 = ((df_solicitacoes_compras[df_solicitacoes_compras['id'].isin([num_solic])])['createdAt']).tolist() 
        data_criacao = pd.to_datetime(x1[0]).date()
        data_hoje = datetime.date.today()
        data_criacao_str = data_criacao.strftime("%d/%m/%Y") 
        data_hoje_str = data_hoje.strftime("%d/%m/%Y")

        
        x2 = ((df_solicitacoes_compras[df_solicitacoes_compras['id'].isin([num_solic])])['requestDate']).tolist()
        data_solic = pd.to_datetime(x2[0]).date()
        data_solic_str = data_solic.strftime("%d/%m/%Y")


        status = ((df_solicitacoes_compras[df_solicitacoes_compras['id'].isin([num_solic])])['status']).to_string(index=False, header=False)
        cod_obra = ((df_solicitacoes_compras[df_solicitacoes_compras['id'].isin([num_solic])])['buildingId']).to_string(index=False, header=False)
        data_hoje = datetime.date.today()

        col1.metric("Data de criação da solicitação de compra nas informações de controle", data_criacao_str)
        col2.metric("Data da solicitação", data_solic_str)
        
        if status == 'Pendente':
            atraso = abs((data_criacao - data_hoje).days)
            col3.metric("Status solicitação de compra", status, f"-{atraso} dias em atraso")
            col4.metric("Código da obra da solicitação", cod_obra)
        
        else:
            col3.metric("Status solicitação de compra", status)
            col4.metric("Código da obra da solicitação", cod_obra)

    st.subheader("Resumo de itens solicitados dos últimos 30 dias", divider="gray")
    dynamic_filters = DynamicFilters(df_itens_compras, filters=['Número da Solicitação', 'Nível de Alçada', 'Autorização'])
    dynamic_filters.display_filters()
    dynamic_filters.display_df()

with aba2:
    st.markdown("Por enquanto essa aba estar sendo produzida. Mas contamos com a sua ajuda com o sugestões de novos Dahs. Anne Monteiro, a linda\
            :tulip:")
