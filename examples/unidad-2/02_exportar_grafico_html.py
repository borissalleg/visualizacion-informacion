"""
Ejemplo (Unidad 2 - Visualización y acceso público)
Exportar un gráfico interactivo de Plotly a HTML autocontenible.
Requiere: pandas, numpy, plotly

Ejecución:
    python 02_exportar_grafico_html.py

Esto genera un archivo "grafico_interactivo.html" que puede abrirse directamente
en cualquier navegador, sin necesidad de un servidor Python corriendo, y puede
subirse a GitHub Pages, Netlify o cualquier hosting estático.
"""
import numpy as np
import pandas as pd
import plotly.express as px

# --- Datos sintéticos: emisiones de CO2 per cápita simuladas por país ---
np.random.seed(1)
paises = ["Colombia", "Brasil", "México", "Argentina", "Chile", "Perú", "Ecuador"]
anios = list(range(2015, 2025))

registros = []
base = {"Colombia": 1.8, "Brasil": 2.3, "México": 3.2, "Argentina": 4.1,
        "Chile": 4.5, "Perú": 1.6, "Ecuador": 2.1}
for pais in paises:
    tendencia = np.cumsum(np.random.normal(0.02, 0.05, size=len(anios)))
    for anio, delta in zip(anios, tendencia):
        registros.append({
            "pais": pais,
            "anio": anio,
            "emisiones_co2_per_capita": round(base[pais] + delta, 3),
        })

df = pd.DataFrame(registros)

# --- Gráfico interactivo de líneas ---
fig = px.line(
    df, x="anio", y="emisiones_co2_per_capita", color="pais",
    title="Emisiones de CO2 per cápita simuladas (2015-2024)",
    labels={"anio": "Año", "emisiones_co2_per_capita": "Toneladas de CO2 per cápita",
            "pais": "País"},
    markers=True,
)
fig.update_layout(hovermode="x unified", template="plotly_white")

# --- Exportar como HTML autocontenible ---
fig.write_html(
    "grafico_interactivo.html",
    include_plotlyjs="cdn",   # usa el CDN de Plotly.js en lugar de embebido (archivo más liviano)
    full_html=True,
    config={"displayModeBar": True, "responsive": True},
)

print("Archivo 'grafico_interactivo.html' generado exitosamente.")
