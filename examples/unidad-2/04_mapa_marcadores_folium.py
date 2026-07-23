"""
Ejemplo (Unidad 2 - Visualizaciones con mapas)
Mapa interactivo con marcadores desde un CSV de coordenadas.
Requiere: folium, pandas

Ejecución:
    python 04_mapa_marcadores_folium.py

Genera un archivo "mapa_sucursales.html" que puede abrirse en cualquier
navegador o publicarse como página estática.
"""
import io

import folium
import pandas as pd
from folium.plugins import MarkerCluster

# --- 1. Dataset sintético de sucursales (equivalente a leer un CSV real) ---
csv_sintetico = """nombre,ciudad,lat,lon,ventas_mensuales
Sucursal Poblado,Medellín,6.2087,-75.5679,85000
Sucursal Laureles,Medellín,6.2447,-75.5916,62000
Sucursal Chapinero,Bogotá,4.6486,-74.0628,120000
Sucursal Usaquén,Bogotá,4.6947,-74.0308,98000
Sucursal Granada,Cali,3.4595,-76.5350,71000
Sucursal El Prado,Barranquilla,10.9878,-74.7889,54000
Sucursal Cabecera,Bucaramanga,7.1254,-73.1198,47000
Sucursal Cartagena Centro,Cartagena,10.4236,-75.5518,68000
"""
df = pd.read_csv(io.StringIO(csv_sintetico))
# En un caso real, se leería directamente con:
# df = pd.read_csv("sucursales.csv")

# --- 2. Crear el mapa base centrado en el centroide de las sucursales ---
mapa = folium.Map(
    location=[df["lat"].mean(), df["lon"].mean()],
    zoom_start=6,
    tiles="CartoDB positron",
)

# --- 3. Agrupador de marcadores ---
cluster = MarkerCluster(name="Sucursales").add_to(mapa)

# --- 4. Agregar un marcador por sucursal, con popup informativo ---
for _, fila in df.iterrows():
    color = "green" if fila["ventas_mensuales"] >= 70000 else "orange"
    popup_html = (
        f"<b>{fila['nombre']}</b><br>"
        f"Ciudad: {fila['ciudad']}<br>"
        f"Ventas mensuales: ${fila['ventas_mensuales']:,}"
    )
    folium.Marker(
        location=[fila["lat"], fila["lon"]],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=fila["nombre"],
        icon=folium.Icon(color=color, icon="shopping-cart", prefix="fa"),
    ).add_to(cluster)

# --- 5. Control de capas ---
folium.LayerControl().add_to(mapa)

# --- 6. Guardar como HTML ---
mapa.save("mapa_sucursales.html")
print("Mapa guardado en 'mapa_sucursales.html'")
