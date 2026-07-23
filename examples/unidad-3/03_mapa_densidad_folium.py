"""
Ejemplo 1 (Unidad 3 - Mapas de densidad)
Mapa de calor geográfico con Folium (folium.plugins.HeatMap).
Requiere: folium, numpy, pandas

Ejecución:
    python 03_mapa_densidad_folium.py

Genera "mapa_calor_incidentes.html".
"""
import folium
import numpy as np
import pandas as pd
from folium.plugins import HeatMap

np.random.seed(21)

focos = [
    (6.2442, -75.5812, 300),   # Centro
    (6.2087, -75.5679, 220),   # El Poblado
    (6.2650, -75.5900, 150),   # Robledo
]

puntos = []
for lat_c, lon_c, n in focos:
    lats = np.random.normal(lat_c, 0.006, n)
    lons = np.random.normal(lon_c, 0.006, n)
    puntos.extend(zip(lats, lons))

lats_ruido = np.random.uniform(6.18, 6.30, 100)
lons_ruido = np.random.uniform(-75.62, -75.54, 100)
puntos.extend(zip(lats_ruido, lons_ruido))

df = pd.DataFrame(puntos, columns=["lat", "lon"])

mapa = folium.Map(location=[6.2442, -75.5812], zoom_start=12,
                   tiles="CartoDB dark_matter")

HeatMap(
    data=df[["lat", "lon"]].values.tolist(),
    radius=15,
    blur=20,
    max_zoom=13,
).add_to(mapa)

mapa.save("mapa_calor_incidentes.html")
print(f"Mapa generado con {len(df)} puntos en 'mapa_calor_incidentes.html'")
