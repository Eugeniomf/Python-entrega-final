# TODO: Aquí debes escribir tu código
import streamlit as st
import pandas as pd
st.set_page_config(page_title="Análisis Bancario", layout="wide")
st.title("Análisis de Datos Bancarios")
df = pd.read_csv('data/processed/p4ds-dataset-bancario-limpio.csv')

df['Fecha'] = pd.to_datetime(df['Fecha'])
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

#  -------------------- Gráficos  --------------------

import plotly.express as px

st.subheader("Distribución de Productos")

st.markdown("Proporción de cada producto bancario sobre el total del portfolio.")

conteo_productos = df_filtrado['Producto'].value_counts().reset_index()
conteo_productos.columns = ['Producto', 'Cantidad']

fig6 = px.pie(
    conteo_productos,
    values='Cantidad',
    names='Producto',
    title='Distribución de Productos Bancarios',
)
st.plotly_chart(fig6, use_container_width=True)

st.subheader("Distribución de Montos USD")

fig = px.histogram(
    prestamos,
    x='Monto USD',
    title='Distribución de Montos de Préstamos',
    labels={'Monto USD': 'Monto en USD', 'count': 'Cantidad'},
    nbins=30
)
# Filtro local para el histograma
producto_hist = st.selectbox(
    'Filtrar histograma por tipo de préstamo',
    ['Todos'] + sorted(prestamos['Producto'].unique().tolist())
)

if producto_hist != 'Todos':
    df_hist = prestamos[prestamos['Producto'] == producto_hist]
else:
    df_hist = prestamos.copy()

fig = px.histogram(
    df_hist,
    x='Monto USD',
    title='Distribución de Montos de Préstamos',
    labels={'Monto USD': 'Monto en USD', 'count': 'Cantidad'},
    nbins=30
)


st.plotly_chart(fig, use_container_width=True)

st.subheader("Relación entre Tipo de Préstamo y Estado de Mora")

conteo = prestamos.groupby(['Producto', 'estado_mora']).size().reset_index(name='Cantidad')

fig2 = px.bar(
    conteo,
    x='Producto',
    y='Cantidad',
    color='estado_mora',
    barmode='group',
    title='Tipo de Préstamo vs Estado de Mora',
    labels={'Producto': 'Tipo de Préstamo', 'estado_mora': 'Estado de Mora', 'Cantidad': 'Cantidad'},
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Relación entre Cantidad y Monto de Préstamos por Sucursal")

scatter_data = prestamos.groupby('Sucursal').agg(
    Cantidad=('Monto USD', 'count'),
    Monto_Promedio=('Monto USD', 'mean')
).reset_index()

fig3 = px.scatter(
    scatter_data,
    x='Cantidad',
    y='Monto_Promedio',
    text='Sucursal',
    title='Cantidad de Préstamos vs Monto Promedio por Sucursal',
    labels={'Cantidad': 'Cantidad de Préstamos', 'Monto_Promedio': 'Monto Promedio en USD'},
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
Cada punto representa una sucursal. 
- **Arriba a la derecha** → muchos préstamos y de montos altos.
- **Arriba a la izquierda** → pocos préstamos pero de montos altos.
- **Abajo a la derecha** → muchos préstamos pero de montos bajos.
""")

st.subheader("Evolución Mensual de Préstamos")

st.markdown("Cantidad de préstamos otorgados por mes a lo largo del año.")

prestamos_copia = prestamos.copy()
prestamos_copia['Mes'] = prestamos_copia['Fecha'].dt.to_period('M').astype(str)

evolucion = prestamos_copia.groupby('Mes').size().reset_index(name='Cantidad')

fig4 = px.line(
    evolucion,
    x='Mes',
    y='Cantidad',
    title='Evolución Mensual de Préstamos Otorgados',
    labels={'Mes': 'Mes', 'Cantidad': 'Cantidad de Préstamos'},
    markers=True
)

st.plotly_chart(fig4, use_container_width=True)

st.subheader("Monto Total por Vendedor")

st.markdown("Dinero que gestionó cada vendedor según sucursal y tipo de préstamo.")

col1, col2 = st.columns(2)

with col1:
    sucursal_vendedor = st.selectbox(
        'Sucursal',
        ['Todas'] + sorted(prestamos['Sucursal'].unique().tolist()),
        key='sucursal_vendedor'
    )

with col2:
    producto_vendedor = st.selectbox(
        'Tipo de Préstamo',
        ['Todos'] + sorted(prestamos['Producto'].unique().tolist()),
        key='producto_vendedor'
    )

df_vendedor = prestamos.copy()

if sucursal_vendedor != 'Todas':
    df_vendedor = df_vendedor[df_vendedor['Sucursal'] == sucursal_vendedor]

if producto_vendedor != 'Todos':
    df_vendedor = df_vendedor[df_vendedor['Producto'] == producto_vendedor]

monto_vendedor = df_vendedor.groupby('Vendedor')['Monto USD'].sum().reset_index()
monto_vendedor = monto_vendedor.sort_values('Monto USD', ascending=False)

fig5 = px.bar(
    monto_vendedor,
    x='Vendedor',
    y='Monto USD',
    title='Monto Total Gestionado por Vendedor',
    labels={'Vendedor': 'Vendedor', 'Monto USD': 'Monto Total en USD'},
    color='Monto USD',
    color_continuous_scale='blues'
)

st.plotly_chart(fig5, use_container_width=True)

