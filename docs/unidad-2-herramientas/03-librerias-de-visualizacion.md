## Librerías de visualización

> ### Objetivos de aprendizaje
> Al finalizar este subtema, el estudiante será capaz de:
>
> - Comparar las principales librerías de visualización (Matplotlib, Seaborn,
>   Plotly, Bokeh, D3.js, ggplot2) según su propósito, curva de aprendizaje e
>   interactividad.
> - Implementar el mismo gráfico con al menos tres librerías distintas de Python
>   para contrastar sintaxis y resultado.
> - Seleccionar la librería más adecuada según el contexto del proyecto.

=== "1. Panorama de librerías"

    No existe una librería "mejor" en términos absolutos: la elección depende del
    objetivo (exploración rápida vs. producto final), la necesidad de interactividad,
    el público destinatario y el ecosistema tecnológico del proyecto.

    | Librería | Lenguaje | Tipo de salida | Interactividad | Curva de aprendizaje | Caso de uso típico |
    |---|---|---|---|---|---|
    | **Matplotlib** | Python | Estática (PNG, SVG, PDF) | Baja (nativa) | Media | Publicaciones científicas, control fino de cada elemento |
    | **Seaborn** | Python (sobre Matplotlib) | Estática | Baja (nativa) | Baja | Análisis estadístico exploratorio, gráficos con buen estilo por defecto |
    | **Plotly** | Python / JS | Interactiva (HTML/JS) | Alta | Baja-media | Dashboards, gráficos web, exploración con zoom/tooltip |
    | **Bokeh** | Python | Interactiva (HTML/JS) | Alta | Media | Aplicaciones web de datos, streaming de datos en el navegador |
    | **D3.js** | JavaScript | Interactiva (SVG/Canvas) | Muy alta (total control) | Alta | Visualizaciones a medida, periodismo de datos, piezas únicas |
    | **ggplot2** | R | Estática (o interactiva vía `plotly::ggplotly`) | Baja (nativa) | Media | Análisis estadístico en R, "gramática de gráficos" (Grammar of Graphics) |

    !!! note "La Gramática de los Gráficos (Grammar of Graphics)"
        Tanto `ggplot2` como, en menor medida, `plotnine` (su equivalente en Python)
        se basan en la teoría de Leland Wilkinson de la **Gramática de los Gráficos**:
        todo gráfico se construye combinando capas (datos, estética/*aesthetics*,
        geometrías, escalas, facetas, coordenadas y temas). Esta aproximación
        declarativa contrasta con el estilo más imperativo de Matplotlib, donde cada
        elemento se agrega paso a paso.

    **¿Cuándo elegir cada una?**

    - **Matplotlib**: cuando necesitas control absoluto sobre cada píxel del gráfico
      (por ejemplo, para una figura de un artículo científico con requisitos
      editoriales estrictos).
    - **Seaborn**: cuando haces análisis exploratorio de datos (EDA) y quieres
      gráficos estadísticos (boxplots, violin plots, pairplots) con muy poco código.
    - **Plotly**: cuando el resultado final debe ser interactivo y consumirse en un
      navegador (dashboards, reportes web).
    - **Bokeh**: alternativa a Plotly cuando se requiere integrar la visualización
      directamente en aplicaciones Python del lado del servidor (Bokeh Server) con
      actualización en tiempo real.
    - **D3.js**: cuando el proyecto requiere una visualización completamente a medida,
      sin las restricciones de una librería de "alto nivel", y se cuenta con
      experiencia en JavaScript/SVG.
    - **ggplot2**: cuando el flujo de análisis ya está en R y se busca aprovechar la
      expresividad de la gramática de gráficos.

=== "2. Ejemplo comparativo"

    A continuación se construye el mismo gráfico (dispersión de esperanza de vida vs.
    PIB per cápita, con tamaño de burbuja proporcional a la población, usando un
    dataset sintético estilo *gapminder*) con **Matplotlib**, **Seaborn** y **Plotly**,
    para contrastar la sintaxis y el resultado.

    **Datos comunes**

    ```python
    """
    Datos sintéticos compartidos para el ejemplo comparativo de librerías.
    Requiere: pandas, numpy
    """
    import numpy as np
    import pandas as pd

    np.random.seed(10)
    paises = ["Colombia", "Brasil", "México", "Argentina", "Chile", "Perú",
              "Ecuador", "Bolivia", "Uruguay", "Paraguay"]

    df = pd.DataFrame({
        "pais": paises,
        "pib_per_capita": np.random.uniform(4000, 25000, size=len(paises)).round(0),
        "esperanza_vida": np.random.uniform(70, 82, size=len(paises)).round(1),
        "poblacion_millones": np.random.uniform(3, 220, size=len(paises)).round(1),
    })
    print(df)
    ```

    === "Matplotlib"

        ```python
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 5))
        scatter = ax.scatter(
            df["pib_per_capita"], df["esperanza_vida"],
            s=df["poblacion_millones"] * 3,  # tamaño de burbuja
            alpha=0.6, c=range(len(df)), cmap="viridis",
        )
        for _, row in df.iterrows():
            ax.annotate(row["pais"], (row["pib_per_capita"], row["esperanza_vida"]),
                        fontsize=8, xytext=(4, 4), textcoords="offset points")
        ax.set_xlabel("PIB per cápita (USD)")
        ax.set_ylabel("Esperanza de vida (años)")
        ax.set_title("Esperanza de vida vs. PIB per cápita (Matplotlib)")
        plt.tight_layout()
        plt.savefig("comparativa_matplotlib.png", dpi=150)
        plt.show()

        # Salida esperada: gráfico estático PNG con burbujas de tamaño proporcional
        # a la población y etiquetas de país anotadas manualmente.
        ```

    === "Seaborn"

        ```python
        import matplotlib.pyplot as plt
        import seaborn as sns

        plt.figure(figsize=(8, 5))
        sns.scatterplot(
            data=df, x="pib_per_capita", y="esperanza_vida",
            size="poblacion_millones", sizes=(50, 500),
            hue="pais", legend=False, alpha=0.7,
        )
        plt.title("Esperanza de vida vs. PIB per cápita (Seaborn)")
        plt.xlabel("PIB per cápita (USD)")
        plt.ylabel("Esperanza de vida (años)")
        plt.tight_layout()
        plt.savefig("comparativa_seaborn.png", dpi=150)
        plt.show()

        # Salida esperada: gráfico estático similar al de Matplotlib, pero con
        # menos líneas de código gracias a los estilos y paletas por defecto de
        # Seaborn (aunque sin etiquetas de texto por país, que requerirían
        # combinarse con matplotlib.pyplot.annotate como en el ejemplo anterior).
        ```

    === "Plotly"

        ```python
        import plotly.express as px

        fig = px.scatter(
            df, x="pib_per_capita", y="esperanza_vida",
            size="poblacion_millones", color="pais", text="pais",
            title="Esperanza de vida vs. PIB per cápita (Plotly)",
            labels={"pib_per_capita": "PIB per cápita (USD)",
                    "esperanza_vida": "Esperanza de vida (años)"},
            size_max=60,
        )
        fig.update_traces(textposition="top center")
        fig.update_layout(template="plotly_white")
        fig.write_html("comparativa_plotly.html", include_plotlyjs="cdn")
        fig.show()

        # Salida esperada: gráfico HTML interactivo (zoom, pan, tooltip al pasar
        # el cursor con todos los valores del país) exportado como archivo
        # "comparativa_plotly.html", además de abrirse en el navegador o notebook.
        ```

    !!! tip "Buenas prácticas"
        Cuando compares librerías para un proyecto real, evalúa no solo la sintaxis
        sino también: (1) el tamaño del archivo/dependencias que agrega al proyecto,
        (2) el rendimiento con datasets grandes (Bokeh y Plotly pueden volverse lentos
        con más de ~100,000 puntos sin técnicas de *downsampling* o *WebGL*), y (3) la
        facilidad de mantenimiento a largo plazo por el equipo.

    !!! warning "Errores comunes"
        Usar Plotly o Bokeh únicamente por su atractivo visual cuando el resultado
        final será un documento estático (PDF, imagen impresa) es contraproducente:
        se pierde toda la interactividad y se paga un costo de dependencias y tiempo
        de renderizado sin beneficio real. En esos casos, Matplotlib o Seaborn siguen
        siendo más eficientes.

!!! example "Ejercicio propuesto"
    1. Usando el dataset `iris` (`sns.load_dataset("iris")`), construye el mismo
       gráfico de dispersión (largo vs. ancho de sépalo, coloreado por especie)
       con Matplotlib, Seaborn y Plotly.
    2. Cronometra cuántas líneas de código necesitó cada implementación y
       compáralas en una tabla.
    3. Exporta la versión de Plotly como HTML y ábrela en un navegador; identifica
       al menos 3 interacciones que no serían posibles con la versión de
       Matplotlib (por ejemplo, zoom, ocultar una categoría desde la leyenda,
       exportar la imagen desde el gráfico mismo).

## Referencias

- Wilkinson, L. (2005). *The Grammar of Graphics* (2nd ed.). Springer.
- Documentación oficial de Matplotlib: <https://matplotlib.org/stable/>
- Documentación oficial de Seaborn: <https://seaborn.pydata.org/>
- Documentación oficial de Plotly: <https://plotly.com/python/>
- Documentación oficial de Bokeh: <https://docs.bokeh.org/>
- Documentación oficial de D3.js: <https://d3js.org/>
- Wickham, H. (2016). *ggplot2: Elegant Graphics for Data Analysis* (2nd ed.).
  Springer.
