"""
Ejemplo 2 (Unidad 3 - Mapas coropléticos)
Mapa coroplético con GeoPandas + Matplotlib (geometrías sintéticas).
Requiere: geopandas, shapely, pandas, matplotlib

Ejecución:
    python 02_mapa_coropletico_geopandas.py
"""
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import box

# --- 1. Construcción de un GeoDataFrame sintético: 6 "departamentos" como
# --- rectángulos dispuestos en una cuadrícula.
nombres = ["Depto A", "Depto B", "Depto C", "Depto D", "Depto E", "Depto F"]
geometrias = [
    box(0, 0, 1, 1), box(1, 0, 2, 1), box(2, 0, 3, 1),
    box(0, 1, 1, 2), box(1, 1, 2, 2), box(2, 1, 3, 2),
]
poblacion_millones = [1.2, 2.5, 0.8, 3.1, 1.9, 0.5]
area_km2 = [8000, 15000, 4000, 22000, 9500, 3000]

gdf = gpd.GeoDataFrame({
    "departamento": nombres,
    "poblacion_millones": poblacion_millones,
    "area_km2": area_km2,
    "geometry": geometrias,
}, crs="EPSG:4326")

# --- 2. Normalización correcta: densidad poblacional (habitantes/km²) ---
gdf["densidad_hab_km2"] = (gdf["poblacion_millones"] * 1_000_000) / gdf["area_km2"]

print(gdf[["departamento", "poblacion_millones", "area_km2", "densidad_hab_km2"]]
      .round(2))

# --- 3. Visualización: comparar valor absoluto (población) vs. normalizado (densidad) ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

gdf.plot(column="poblacion_millones", cmap="OrRd", legend=True, ax=axes[0],
         edgecolor="black", linewidth=0.5)
axes[0].set_title("Población total (millones)\n— sin normalizar —")
axes[0].axis("off")

gdf.plot(column="densidad_hab_km2", cmap="OrRd", legend=True, ax=axes[1],
         edgecolor="black", linewidth=0.5)
axes[1].set_title("Densidad poblacional (hab/km²)\n— normalizado por área —")
axes[1].axis("off")

for ax in axes:
    for _, row in gdf.iterrows():
        centro = row["geometry"].centroid
        ax.annotate(row["departamento"], (centro.x, centro.y), ha="center",
                    fontsize=8, color="black")

plt.tight_layout()
plt.savefig("mapa_coropletico_geopandas.png", dpi=150)
plt.show()
