## Mapas de densidad

> ### Objetivos de aprendizaje
> Al finalizar este subtema, el estudiante será capaz de:
>
> - Explicar el concepto de mapa de calor (heatmap) geográfico y su diferencia con un
>   mapa de marcadores o un mapa coroplético.
> - Comprender los fundamentos de la estimación de densidad por kernel (KDE, *Kernel
>   Density Estimation*).
> - Construir un mapa de densidad geográfico con Folium (`HeatMap`) y una estimación
>   de densidad con `seaborn.kdeplot`.

=== "1. ¿Qué es un mapa de densidad?"

    Un **mapa de densidad** (o *heatmap* geográfico) representa la **concentración
    espacial** de eventos o puntos, sin necesidad de agregarlos previamente a
    regiones administrativas (como sí requiere un mapa coroplético). Es la
    herramienta ideal cuando se tienen muchas observaciones puntuales (ej. ubicación
    de accidentes de tránsito, delitos reportados, avistamientos de fauna) y se busca
    identificar visualmente **"puntos calientes"** (*hotspots*) de mayor concentración.

    | Técnica | Unidad de análisis | Requiere fronteras administrativas | Mejor para |
    |---|---|---|---|
    | Mapa de marcadores | Punto individual | No | Pocos puntos, cada uno relevante individualmente |
    | Mapa coroplético | Región agregada | Sí | Comparar regiones entre sí con una variable normalizada |
    | **Mapa de densidad** | Concentración continua | No | Miles de puntos, identificar zonas de alta concentración |

=== "2. Estimación de densidad por kernel (KDE)"

    La **estimación de densidad por kernel** es una técnica estadística no
    paramétrica que estima la función de densidad de probabilidad subyacente a partir
    de una muestra de puntos, sin asumir una distribución específica (como la normal).
    Para cada punto del espacio, KDE calcula un valor de densidad sumando las
    contribuciones de "núcleos" (*kernels*, típicamente gaussianos) centrados en cada
    observación:

    $$
    \hat{f}(x) = \frac{1}{nh} \sum_{i=1}^{n} K\left(\frac{x - x_i}{h}\right)
    $$

    donde $n$ es el número de observaciones, $h$ es el **ancho de banda**
    (*bandwidth*) —que controla el grado de suavizado— y $K$ es la función kernel
    (usualmente gaussiana). En el contexto geográfico, esta misma lógica se aplica en
    dos dimensiones (latitud y longitud), generando una superficie continua de
    densidad que se visualiza mediante gradientes de color (típicamente de azul/verde
    para baja densidad a rojo/amarillo para alta densidad).

    !!! note "El rol crítico del ancho de banda (bandwidth)"
        Un ancho de banda **muy pequeño** genera un mapa "ruidoso", con muchos picos
        aislados que sobreajustan a los puntos individuales (similar a un
        *overfitting*). Un ancho de banda **muy grande** sobre-suaviza el resultado,
        ocultando concentraciones reales y generando un único "montículo" difuso. La
        elección del ancho de banda debe balancear detalle y generalización, y
        frecuentemente se ajusta visualmente o mediante reglas como la de Silverman.

    !!! warning "Errores comunes"
        Interpretar un mapa de calor sin considerar la **densidad poblacional de
        fondo** puede llevar a conclusiones erróneas: un "punto caliente" de delitos
        reportados puede simplemente reflejar una zona con mayor población o mayor
        tránsito peatonal, no necesariamente una zona intrínsecamente más peligrosa
        per cápita. Al igual que con los mapas coropléticos, es importante considerar
        si el fenómeno debería normalizarse respecto a una variable de exposición
        (población, tráfico, horas de operación).

=== "3. Ejemplos de código"

    === "Folium HeatMap"

        ```python
        """
        Ejemplo 1: Mapa de calor geográfico con Folium (folium.plugins.HeatMap).
        Requiere: folium, numpy, pandas

        Ejecución:
            python mapa_densidad_folium.py

        Genera "mapa_calor_incidentes.html".
        """
        import folium
        import numpy as np
        import pandas as pd
        from folium.plugins import HeatMap

        # --- 1. Datos sintéticos: ubicaciones de "incidentes" concentrados alrededor
        # --- de 3 focos (clusters) dentro del área urbana de Medellín, más ruido de
        # --- fondo disperso en toda la ciudad.
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

        # Ruido de fondo disperso en toda la ciudad
        lats_ruido = np.random.uniform(6.18, 6.30, 100)
        lons_ruido = np.random.uniform(-75.62, -75.54, 100)
        puntos.extend(zip(lats_ruido, lons_ruido))

        df = pd.DataFrame(puntos, columns=["lat", "lon"])

        # --- 2. Construcción del mapa base ---
        mapa = folium.Map(location=[6.2442, -75.5812], zoom_start=12,
                           tiles="CartoDB dark_matter")  # fondo oscuro resalta el heatmap

        # --- 3. Capa de mapa de calor ---
        HeatMap(
            data=df[["lat", "lon"]].values.tolist(),
            radius=15,      # equivalente aproximado al "ancho de banda" visual
            blur=20,
            max_zoom=13,
        ).add_to(mapa)

        mapa.save("mapa_calor_incidentes.html")
        print(f"Mapa generado con {len(df)} puntos en 'mapa_calor_incidentes.html'")

        # Salida esperada:
        # Un mapa oscuro de Medellín con tres zonas claramente resaltadas en tonos
        # rojo/amarillo (los tres focos simulados: Centro, El Poblado y Robledo),
        # rodeadas de un halo verde/azul que se desvanece hacia zonas de menor
        # concentración, y puntos de "ruido de fondo" dispersos apenas visibles en
        # el resto de la ciudad.
        ```

    === "Seaborn KDE"

        Este ejemplo ilustra el concepto matemático de KDE directamente sobre las
        coordenadas (sin un mapa base), útil para entender el efecto del ancho de banda
        antes de aplicarlo sobre un mapa real.

        ```python
        """
        Ejemplo 2: Estimación de densidad por kernel (KDE) con Seaborn.
        Requiere: seaborn, matplotlib, numpy, pandas

        Ejecución:
            python kde_densidad_seaborn.py
        """
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        import seaborn as sns

        np.random.seed(21)
        focos = [(6.2442, -75.5812, 300), (6.2087, -75.5679, 220), (6.2650, -75.5900, 150)]
        puntos = []
        for lat_c, lon_c, n in focos:
            lats = np.random.normal(lat_c, 0.006, n)
            lons = np.random.normal(lon_c, 0.006, n)
            puntos.extend(zip(lats, lons))

        df = pd.DataFrame(puntos, columns=["lat", "lon"])

        fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

        for ax, bw in zip(axes, [0.1, 0.5, 2.0]):
            sns.kdeplot(
                data=df, x="lon", y="lat", fill=True, cmap="rocket_r",
                bw_adjust=bw, thresh=0.05, ax=ax,
            )
            sns.scatterplot(data=df, x="lon", y="lat", s=5, color="black", alpha=0.3, ax=ax)
            ax.set_title(f"bw_adjust = {bw}")

        plt.suptitle("Efecto del ancho de banda (bandwidth) en la estimación KDE")
        plt.tight_layout()
        plt.savefig("kde_densidad_seaborn.png", dpi=150)
        plt.show()

        # Salida esperada:
        # Tres paneles con la misma nube de puntos (representando los 3 focos
        # simulados de incidentes). El panel con bw_adjust=0.1 muestra una densidad
        # "ruidosa" con múltiples picos aislados que casi calcan cada punto
        # individual; el panel con bw_adjust=0.5 muestra tres focos de densidad bien
        # definidos y separados (el ajuste más informativo); el panel con
        # bw_adjust=2.0 muestra un único "montículo" difuso que combina los tres
        # focos, perdiendo la capacidad de distinguirlos.
        ```

    !!! tip "Buenas prácticas"
        - Prueba distintos valores de ancho de banda (`radius`/`blur` en Folium,
          `bw_adjust` en Seaborn) y elige el que revele la estructura real de los
          datos sin ser demasiado ruidoso ni demasiado suave.
        - Usa mapas base oscuros o minimalistas (`CartoDB dark_matter`,
          `CartoDB positron`) para que el gradiente de color del heatmap resalte con
          buen contraste.
        - Cuando sea posible, complementa el mapa de calor con una normalización
          respecto a una variable de exposición relevante (población, tráfico,
          horas-persona), especialmente antes de comunicar conclusiones sobre "zonas
          de riesgo".

!!! example "Ejercicio propuesto"
    1. Modifica el ejemplo de Folium para simular 5 focos de "reportes de
       basuras" en distintas comunas de tu ciudad, con distinta intensidad
       (número de puntos) cada uno.
    2. Experimenta con al menos 3 combinaciones de `radius` y `blur` en
       `HeatMap` y documenta (con capturas de pantalla) cómo cambia la
       interpretación visual del mapa.
    3. Investiga la "regla de Silverman" para la selección automática del ancho
       de banda en KDE y aplícala (usando `scipy.stats.gaussian_kde`) sobre el
       dataset del Ejemplo 2, comparando el resultado con los anchos de banda
       manuales usados en el ejemplo.

## Referencias

- Silverman, B. W. (1986). *Density Estimation for Statistics and Data
  Analysis*. Chapman & Hall.
- Documentación de Folium HeatMap plugin:
  <https://python-visualization.github.io/folium/latest/user_guide/plugins/heatmap.html>
- Documentación de Seaborn `kdeplot`:
  <https://seaborn.pydata.org/generated/seaborn.kdeplot.html>
- Silverman, B. W. Rule of thumb bandwidth — referenciado en
  `scipy.stats.gaussian_kde`: <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html>
