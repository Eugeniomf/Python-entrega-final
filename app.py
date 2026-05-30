# TODO: Aquí debes escribir tu código
import streamlit as st
import pandas as pd
st.set_page_config(page_title="Análisis Bancario", layout="wide")
st.title("Análisis Interactivo de Datos Bancarios")
df = pd.read_csv('data/processed/p4ds-dataset-bancario-limpio.csv')



st.sidebar.markdown("## Filtros")
st.sidebar.markdown("Seleccioná los filtros para explorar los datos")

# Filtro por Sucursal
sucursales = ['Todas'] + sorted(df['Sucursal'].unique().tolist())
sucursal_seleccionada = st.sidebar.selectbox('Sucursal', sucursales)
productos = ['Todos'] + sorted(df['Producto'].unique().tolist())
producto_seleccionado = st.sidebar.selectbox('Producto', productos)

estados = ['Todos'] + sorted(df['Estado App'].unique().tolist())
estado_seleccionado = st.sidebar.selectbox('Estado App', estados)

estados_mora = ['Todos'] + sorted(df['estado_mora'].dropna().unique().tolist())
estado_mora_seleccionado = st.sidebar.selectbox('Estado Mora', estados_mora)

# Aplicar filtro
df_filtrado = df.copy()

if sucursal_seleccionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Sucursal'] == sucursal_seleccionada]

if producto_seleccionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Producto'] == producto_seleccionado]

if estado_seleccionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Estado App'] == estado_seleccionado]

if estado_mora_seleccionado != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['estado_mora'] == estado_mora_seleccionado]

st.dataframe(df_filtrado)

