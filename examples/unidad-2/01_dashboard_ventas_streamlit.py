"""
Ejemplo (Unidad 2 - Cuadros de mando)
Dashboard estratégico de ventas con Streamlit.
Requiere: streamlit, pandas, numpy, plotly

Ejecución:
    streamlit run 01_dashboard_ventas_streamlit.py
"""
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

# --- 1. Generación de datos sintéticos ---
np.random.seed(3)
fechas = pd.date_range("2025-01-01", "2025-12-31", freq="D")
departamentos = ["Antioquia", "Bogotá D.C.", "Valle del Cauca", "Atlántico", "Santander"]
lineas_producto = ["Electrónica", "Hogar", "Moda", "Alimentos"]

df = pd.DataFrame({
    "fecha": np.random.choice(fechas, size=3000),
    "departamento": np.random.choice(departamentos, size=3000),
    "linea_producto": np.random.choice(lineas_producto, size=3000),
    "monto": np.random.gamma(shape=2.0, scale=80, size=3000).round(2),
})
df["mes"] = df["fecha"].dt.to_period("M").astype(str)

# --- 2. Barra lateral: filtros (segmentadores, equivalentes a los slicers de Power BI) ---
st.sidebar.header("Filtros")
depto_sel = st.sidebar.multiselect("Departamento", departamentos, default=departamentos)
linea_sel = st.sidebar.multiselect("Línea de producto", lineas_producto, default=lineas_producto)

df_filtrado = df[df["departamento"].isin(depto_sel) & df["linea_producto"].isin(linea_sel)]

# --- 3. KPI principal (tarjeta, esquina superior izquierda por jerarquía visual) ---
st.title("📊 Dashboard estratégico de ventas — Año 2025")
col1, col2, col3 = st.columns(3)
col1.metric("Ventas totales (YTD)", f"${df_filtrado['monto'].sum():,.0f}")
col2.metric("Ticket promedio", f"${df_filtrado['monto'].mean():,.2f}")
col3.metric("Transacciones", f"{len(df_filtrado):,}")

# --- 4. Gráfico de tendencia mensual ---
tendencia = df_filtrado.groupby("mes")["monto"].sum().reset_index()
fig_tendencia = px.line(tendencia, x="mes", y="monto", title="Tendencia mensual de ventas",
                          markers=True)
st.plotly_chart(fig_tendencia, use_container_width=True)

# --- 5. Distribución por departamento y línea de producto ---
col_a, col_b = st.columns(2)
por_depto = df_filtrado.groupby("departamento")["monto"].sum().sort_values(ascending=False).reset_index()
fig_depto = px.bar(por_depto, x="departamento", y="monto", title="Ventas por departamento")
col_a.plotly_chart(fig_depto, use_container_width=True)

por_linea = df_filtrado.groupby("linea_producto")["monto"].sum().reset_index()
fig_linea = px.pie(por_linea, names="linea_producto", values="monto",
                     title="Participación por línea de producto")
col_b.plotly_chart(fig_linea, use_container_width=True)

# --- 6. Tabla de detalle filtrable ---
with st.expander("Ver datos de detalle"):
    st.dataframe(df_filtrado.sort_values("fecha", ascending=False))
