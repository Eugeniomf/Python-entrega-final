# TODO: Aquí debes escribir tu código
import streamlit as st
import pandas as pd
st.set_page_config(page_title="Análisis Bancario", layout="wide")
st.title("Análisis de Datos Bancarios")
df = pd.read_csv('data/processed/p4ds-dataset-bancario-limpio.csv')

productos_prestamo = ['Préstamo Consumo', 'Préstamo Automotor', 'Préstamo Hipotecario']

st.sidebar.markdown("## Filtros")
st.sidebar.markdown("Seleccioná los filtros para explorar los datos")

# --------------------Filtros --------------------

# Sucursales
sucursales = ['Todas'] + sorted(df['Sucursal'].unique().tolist())
sucursal_seleccionada = st.sidebar.selectbox('Sucursal', sucursales)

# Productos
productos = ['Todos'] + sorted(df['Producto'].unique().tolist())
producto_seleccionado = st.sidebar.selectbox('Producto', productos)

# Estado de la App
estados = ['Todos'] + sorted(df['Estado App'].unique().tolist())
estado_seleccionado = st.sidebar.selectbox('Estado App', estados)

# Estado Mora
estados_mora = ['Todos'] + sorted(df['estado_mora'].dropna().unique().tolist())
estado_mora_seleccionado = st.sidebar.selectbox('Estado Mora', estados_mora)

# -------------------- Aplicar filtros --------------------
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

# -------------------- Resumen Estadístico --------------------

st.subheader("Resumen Estadístico")
st.markdown("""
Las siguientes estadísticas corresponden a la columna **Monto USD**.

Refiere al monto otorgado por las distintas sucursales en concepto de préstamos. 

Podemos filtrar según interese, por sucursal, producto, estado de mora e inclusive por uso de la app.
""")

st.subheader("Distribución por Tipo de Préstamo")

prestamos = df_filtrado[df_filtrado['Producto'].isin(productos_prestamo)]
conteo = prestamos['Producto'].value_counts()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Préstamo Consumo", conteo.get('Préstamo Consumo', 0))
with col2:
    st.metric("Préstamo Automotor", conteo.get('Préstamo Automotor', 0))
with col3:
    st.metric("Préstamo Hipotecario", conteo.get('Préstamo Hipotecario', 0))



col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Media", round(df_filtrado['Monto USD'].mean(), 2))
    st.metric("Mediana", round(df_filtrado['Monto USD'].median(), 2))

with col2:
    st.metric("Desv. Estándar", round(df_filtrado['Monto USD'].std(), 2))
    st.metric("Rango", round(df_filtrado['Monto USD'].max() - df_filtrado['Monto USD'].min(), 2))

with col3:
    st.metric("Máximo", round(df_filtrado['Monto USD'].max(), 2))

with col4:
    st.metric("Q1 (25%)", round(df_filtrado['Monto USD'].quantile(0.25), 2))
    st.metric("Q2 (50%)", round(df_filtrado['Monto USD'].quantile(0.50), 2))
    st.metric("Q3 (75%)", round(df_filtrado['Monto USD'].quantile(0.75), 2))

