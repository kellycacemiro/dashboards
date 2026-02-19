import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração inicial da página
st.set_page_config(page_title="Dashboard Censo 2022 - Campo Grande", layout="wide")
st.title("📊 Dashboard do Censo 2022 - Campo Grande/MS")
st.markdown("Uma visão interativa dos dados demográficos por regiões urbanas.")

# 2. Carregar os dados
@st.cache_data
def carregar_dados():
    # Agora o código procura a planilha na mesma pasta onde ele está:
    arquivo = "CENSO2022_GEMINI.xlsx - CG_CENSO_2022_GEMINI.csv"
    
    df = pd.read_csv(arquivo, encoding='latin-1', sep=';')
    return df
    

df = carregar_dados()

# Separar os dados totais da cidade dos dados dos bairros/regiões
df_total = df[df['NOME'] == 'CAMPO GRANDE-MS']
df_regioes = df[df['NOME'] != 'CAMPO GRANDE-MS'].copy()

# 3. Métricas Principais (Cards no topo)
st.subheader("Resumo da Cidade")
col1, col2, col3, col4 = st.columns(4)

if not df_total.empty:
    pop_2022 = df_total['POPULAÇÃO - 2022'].values[0]
    pop_2010 = df_total['POPULAÇÃO - 2010'].values[0]
    
    # Tratamento do crescimento
    crescimento_bruto = df_total['TAXA MÉDIA GEOMÉTRICA DE CRESCIMENTO ANUAL - 2010/2022'].values[0]
    crescimento = float(str(crescimento_bruto).replace(',', '.'))
    
    domicilios = df_total['DOMICÍLIOS PARTICULARES - 2022'].values[0]
    
    col1.metric("População Total (2022)", f"{pop_2022:,.0f}".replace(",", "."))
    col2.metric("População (2010)", f"{pop_2010:,.0f}".replace(",", "."))
    col3.metric("Crescimento Anual", f"{crescimento:.2f}%")
    col4.metric("Domicílios Particulares", f"{domicilios:,.0f}".replace(",", "."))

st.divider()

# 4. Criando Abas para organizar os gráficos
aba1, aba2, aba3 = st.tabs(["População e Densidade", "Perfil Demográfico", "Infraestrutura Básica"])

with aba1:
    st.subheader("População por Região (2022)")
    # Selecionar top 15 para não poluir o gráfico
    df_pop = df_regioes.sort_values(by='POPULAÇÃO - 2022', ascending=False).head(15)
    fig_pop = px.bar(df_pop, x='NOME', y='POPULAÇÃO - 2022',
                     color='POPULAÇÃO - 2022', color_continuous_scale='Blues',
                     labels={'NOME': 'Região', 'POPULAÇÃO - 2022': 'Habitantes'},
                     text_auto='.2s')
    st.plotly_chart(fig_pop, use_container_width=True)

    st.subheader("Densidade Demográfica (Habitantes / Hectare)")
    df_densidade = df_regioes.sort_values(by='DENSIDADE DEMOGRÁFICA (HAB/HA) - 2022', ascending=False).head(15)
    fig_densidade = px.bar(df_densidade, x='NOME', y='DENSIDADE DEMOGRÁFICA (HAB/HA) - 2022',
                           color='DENSIDADE DEMOGRÁFICA (HAB/HA) - 2022', color_continuous_scale='Oranges',
                           labels={'NOME': 'Região', 'DENSIDADE DEMOGRÁFICA (HAB/HA) - 2022': 'Densidade (Hab/ha)'})
    st.plotly_chart(fig_densidade, use_container_width=True)

with aba2:
    st.subheader("Comparativo: Homens vs Mulheres por Região")
    # Preparar dados para barras agrupadas
    df_sexo = df_regioes[['NOME', 'HOMENS - 2022', 'MULHERES - 2022']].sort_values(by='MULHERES - 2022', ascending=False).head(15)
    df_sexo_melt = df_sexo.melt(id_vars='NOME', var_name='Gênero', value_name='População')
    # Limpando os nomes da legenda
    df_sexo_melt['Gênero'] = df_sexo_melt['Gênero'].str.replace(' - 2022', '')
    
    fig_sexo = px.bar(df_sexo_melt, x='NOME', y='População', color='Gênero', barmode='group',
                      color_discrete_map={'HOMENS': '#1f77b4', 'MULHERES': '#e377c2'})
    st.plotly_chart(fig_sexo, use_container_width=True)

    st.subheader("Índice de Envelhecimento (2022)")
    df_idosos = df_regioes.sort_values(by='ÍNDICE DE ENVELHECIMENTO - 2022', ascending=False).head(15)
    fig_idosos = px.bar(df_idosos, x='NOME', y='ÍNDICE DE ENVELHECIMENTO - 2022',
                        color='ÍNDICE DE ENVELHECIMENTO - 2022', color_continuous_scale='Purples')
    st.plotly_chart(fig_idosos, use_container_width=True)

with aba3:
    st.subheader("Taxa de Alfabetização (%) - 2022")
    df_alfa = df_regioes.sort_values(by='TAXA DE ALFABETIZAÇÃO (%) - 2022', ascending=False).head(20)
    fig_alfa = px.line(df_alfa, x='NOME', y='TAXA DE ALFABETIZAÇÃO (%) - 2022', markers=True)
    st.plotly_chart(fig_alfa, use_container_width=True)

    st.subheader("Média de Moradores por Domicílio")
    df_moradores = df_regioes.sort_values(by='MÉDIA DE MORADORES - 2022', ascending=False).head(15)
    fig_moradores = px.bar(df_moradores, x='MÉDIA DE MORADORES - 2022', y='NOME', orientation='h',
                           color='MÉDIA DE MORADORES - 2022', color_continuous_scale='Teal')
    st.plotly_chart(fig_moradores, use_container_width=True)


st.sidebar.info("Dashboard gerado com Streamlit e Plotly com base nos dados do Censo IBGE 2022 para Campo Grande/MS.")


