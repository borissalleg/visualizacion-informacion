# **Unidad 3 — Geovisualización**

La **geovisualización** aplica los principios generales de visualización de
información (Unidad 1) y las herramientas vistas en la Unidad 2 al análisis de
datos con un componente espacial explícito. Esta unidad profundiza en tres técnicas
fundamentales para representar variables sobre un territorio: mapas coropléticos,
mapas de densidad e interpolación espacial.

=== "Contenidos"

    | # | Tema | Descripción breve |
    |---|------|--------------------|
    | 1 | [Mapas coropléticos](01-mapas-coropleticos.md) | Regiones coloreadas según una variable, normalización |
    | 2 | [Mapas de densidad](02-mapas-de-densidad.md) | Heatmaps geográficos, kernel density estimation |
    | 3 | [Interpolación espacial](03-interpolacion-espacial.md) | IDW y Kriging para estimar valores en ubicaciones no muestreadas |

=== "Objetivos de la unidad"

    - Construir mapas coropléticos correctamente normalizados usando GeoPandas y
      Plotly.
    - Identificar y evitar errores comunes de normalización en mapas coropléticos.
    - Construir mapas de densidad (heatmaps geográficos) e interpretar el concepto de
      estimación de densidad por kernel (KDE).
    - Aplicar técnicas de interpolación espacial (IDW, Kriging) para estimar valores
      continuos a partir de mediciones puntuales.

!!! note "Duración estimada"
    Se recomienda dedicar entre 8 y 10 horas de estudio a esta unidad. Los
    ejemplos de Kriging requieren fundamentos de estadística espacial y pueden
    tomar más tiempo de asimilación.

!!! warning "Prerrequisitos técnicos"
    Los ejemplos de esta unidad requieren `geopandas`, cuya instalación puede ser
    más compleja que la de librerías puramente Python debido a sus dependencias
    geoespaciales (GDAL, GEOS, PROJ). Se recomienda usar `conda`/`mamba` o los
    entornos de Google Colab si se presentan problemas de instalación con `pip`.
