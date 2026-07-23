"""
Ejemplo 1 (Unidad 3 - Mapas coropléticos)
Mapa coroplético de países con Plotly Express.
Requiere: pandas, plotly

Ejecución:
    python 01_mapa_coropletico_plotly.py
"""
import pandas as pd
import plotly.express as px

# --- Datos sintéticos: tasa de acceso a internet (%) e ISO-3 de países de
# --- América Latina, normalizados como porcentaje (0-100).
df = pd.DataFrame({
    "pais": ["Colombia", "Brasil", "México", "Argentina", "Chile", "Perú",
             "Ecuador", "Bolivia", "Uruguay", "Paraguay", "Venezuela"],
    "iso_alpha": ["COL", "BRA", "MEX", "ARG", "CHL", "PER", "ECU", "BOL", "URY",
                  "PRY", "VEN"],
    "acceso_internet_pct": [67.2, 74.0, 71.5, 87.2, 88.3, 71.0, 68.5, 55.0, 78.9,
                             65.4, 72.0],
})

fig = px.choropleth(
    df,
    locations="iso_alpha",
    color="acceso_internet_pct",
    hover_name="pais",
    color_continuous_scale="YlGnBu",
    range_color=(50, 90),
    scope="south america",
    labels={"acceso_internet_pct": "Acceso a internet (%)"},
    title="Acceso a internet por país (datos simulados, % de la población)",
)
fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))
fig.write_html("mapa_coropletico_plotly.html", include_plotlyjs="cdn")
print("Archivo 'mapa_coropletico_plotly.html' generado exitosamente.")
