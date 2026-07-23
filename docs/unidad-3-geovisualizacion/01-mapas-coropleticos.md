# Mapas coropléticos

## Objetivos de aprendizaje

Al finalizar este subtema, el estudiante será capaz de:

- Definir qué es un mapa coroplético y en qué escenarios es apropiado usarlo.
- Identificar el error común de normalización por área vs. normalización por
  variable relevante.
- Construir mapas coropléticos con Plotly (usando códigos ISO de país) y con
  GeoPandas + Matplotlib (usando geometrías propias).

## 1. ¿Qué es un mapa coroplético?

Un **mapa coroplético** (del griego *choros*, "lugar", y *plethos*, "multitud")
representa el valor de una variable mediante la **intensidad de color** de
regiones geográficas predefinidas (países, departamentos, municipios, códigos
postales). Es una de las formas más comunes de geovisualización porque se apoya en
límites administrativos que la audiencia ya reconoce.

!!! note "¿Cuándo usar un mapa coroplético?"
    Es apropiado cuando la variable de interés tiene sentido **agregada a nivel de
    región** (por ejemplo, tasa de desempleo departamental, densidad poblacional,
    resultado electoral por municipio). No es apropiado para representar
    ubicaciones puntuales individuales (para eso, ver mapas de marcadores, Unidad
    2) ni para representar fenómenos continuos sin fronteras naturales claras
    (para eso, ver mapas de densidad e interpolación espacial, más adelante en
    esta unidad).

## 2. El error de normalización: por área vs. por variable relevante

El error más frecuente al construir mapas coropléticos es representar un **valor
absoluto** (por ejemplo, población total, número de casos) en lugar de un
**valor normalizado** (por ejemplo, población por km², tasa de casos por 100,000
habitantes). Esto es problemático porque las regiones más grandes en área o más
pobladas tienden a mostrar valores absolutos más altos simplemente por su tamaño,
no porque el fenómeno subyacente sea más intenso allí.

| Enfoque | Qué representa | Riesgo |
|---|---|---|
| **Valor absoluto** (ej. total de casos de una enfermedad) | Magnitud bruta | Sobrerrepresenta regiones grandes o muy pobladas |
| **Normalizado por población** (ej. casos por 100,000 habitantes) | Intensidad relativa a la población | Correcto para comparar "riesgo" o "prevalencia" |
| **Normalizado por área** (ej. población por km²) | Densidad espacial | Correcto para comparar concentración territorial, no para tasas per cápita |

!!! warning "Errores comunes"
    Un mapa coroplético que muestra el "número total de contagios por
    departamento" durante una epidemia sin normalizar por población dará la
    impresión de que los departamentos más poblados (ej. con ciudades capitales
    grandes) son los "más afectados", cuando en realidad podrían tener una tasa de
    contagio per cápita menor que un departamento pequeño con un brote
    proporcionalmente más severo. **Siempre pregúntate: ¿qué pregunta responde la
    normalización elegida?**

!!! tip "Buenas prácticas"
    - Usa escalas de color **secuenciales** (de un tono claro a uno oscuro) para
      variables continuas con un único sentido (ej. de "menos" a "más").
    - Usa escalas **divergentes** (dos tonos que se alejan de un punto central,
      ej. azul-blanco-rojo) cuando el dato tiene un punto de referencia natural
      (ej. variación porcentual respecto al año anterior: negativo vs. positivo).
    - Evita más de 5-7 categorías o "bins" de color: dificulta distinguir tonos
      intermedios.
    - Incluye siempre una leyenda con la escala de color y las unidades de la
      variable representada.

## 3. Ejemplo 1: mapa coroplético con Plotly (códigos ISO de país)

Plotly incluye un mapa mundial base y reconoce automáticamente los códigos ISO-3 de
país, por lo que no es necesario cargar un archivo GeoJSON externo para mapas a
nivel de país.

```python
"""
Ejemplo 1: Mapa coroplético de países con Plotly Express.
Requiere: pandas, plotly

Ejecución:
    python mapa_coropletico_plotly.py
"""
import pandas as pd
import plotly.express as px

# --- Datos sintéticos: tasa de acceso a internet (%) e ISO-3 de países de
# --- América Latina, normalizados como porcentaje (0-100), no como valores
# --- absolutos de usuarios (para evitar el error de normalización).
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
    color_continuous_scale="YlGnBu",  # escala secuencial (variable de un solo sentido)
    range_color=(50, 90),
    scope="south america",
    labels={"acceso_internet_pct": "Acceso a internet (%)"},
    title="Acceso a internet por país (datos simulados, % de la población)",
)
fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))
fig.write_html("mapa_coropletico_plotly.html", include_plotlyjs="cdn")
fig.show()

# Salida esperada:
# Un mapa de América del Sur/Latinoamérica con cada país coloreado según su
# tasa (normalizada, en porcentaje) de acceso a internet, usando una escala de
# color secuencial de amarillo claro (menor acceso) a azul oscuro (mayor
# acceso). Al pasar el cursor sobre un país se muestra su nombre y el valor
# exacto.
```

## 4. Ejemplo 2: mapa coroplético con GeoPandas + Matplotlib (geometrías propias)

Cuando se trabaja a nivel de departamentos o municipios (sin códigos ISO
estandarizados globalmente), es común construir o cargar un `GeoDataFrame` con las
geometrías (polígonos) de cada región. Este ejemplo construye geometrías
sintéticas simplificadas (rectángulos) para simular departamentos y evitar
depender de un archivo GeoJSON externo, manteniendo el ejemplo autocontenible.

```python
"""
Ejemplo 2: Mapa coroplético con GeoPandas + Matplotlib (geometrías sintéticas).
Requiere: geopandas, shapely, pandas, matplotlib

Ejecución:
    python mapa_coropletico_geopandas.py
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import box

# --- 1. Construcción de un GeoDataFrame sintético: 6 "departamentos" como
# --- rectángulos dispuestos en una cuadrícula (simula un mapa administrativo
# --- simplificado sin necesidad de un GeoJSON externo).
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

# Etiquetas con el nombre de cada departamento
for ax in axes:
    for _, row in gdf.iterrows():
        centro = row["geometry"].centroid
        ax.annotate(row["departamento"], (centro.x, centro.y), ha="center",
                    fontsize=8, color="black")

plt.tight_layout()
plt.savefig("mapa_coropletico_geopandas.png", dpi=150)
plt.show()

# Salida esperada:
# Dos mapas lado a lado con la misma geometría de 6 departamentos sintéticos.
# El de la izquierda colorea según población absoluta (Depto D, el más
# poblado, se ve más "intenso" simplemente por tener más habitantes). El de
# la derecha colorea según densidad poblacional (normalizada por área),
# mostrando que Depto C —pequeño en área pero con población moderada— puede
# tener una densidad relativa distinta a la que sugiere el mapa sin
# normalizar, evidenciando el efecto de la normalización sobre la
# interpretación del mapa.
```

## Ejercicio propuesto

!!! example "Ejercicio propuesto"
    1. Descarga un GeoJSON real de los departamentos de Colombia (por ejemplo,
       desde el portal de datos abiertos del DANE o repositorios públicos de
       límites administrativos) y colócalo en `docs/assets/datasets/`.
    2. Construye un mapa coroplético con GeoPandas mostrando una variable
       normalizada de tu elección (ej. densidad poblacional, tasa de
       alfabetización).
    3. Construye una segunda versión del mismo mapa usando el valor absoluto (sin
       normalizar) y compara visualmente ambos resultados. Redacta un párrafo
       explicando qué conclusiones erróneas podría sacar un lector si solo viera
       la versión sin normalizar.

## Referencias

- Slocum, T. A., McMaster, R. B., Kessler, F. C., & Howard, H. H. (2009).
  *Thematic Cartography and Geovisualization* (3rd ed.). Pearson Prentice Hall.
- Documentación oficial de GeoPandas: <https://geopandas.org/>
- Documentación oficial de Plotly Choropleth Maps:
  <https://plotly.com/python/choropleth-maps/>
- DANE — División Político-Administrativa de Colombia (DIVIPOLA):
  <https://www.dane.gov.co/>
