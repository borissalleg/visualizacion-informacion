## Visualización y acceso público

> ### Objetivos de aprendizaje
> Al finalizar este subtema, el estudiante será capaz de:
>
> - Identificar los principales portales de datos abiertos disponibles en Colombia y
>   el mundo.
> - Reconocer distintos canales para publicar visualizaciones de acceso público
>   (GitHub Pages, Tableau Public, Observable).
> - Exportar y publicar un gráfico interactivo como archivo HTML autocontenible.

=== "1. Portales de datos abiertos"

    Los **portales de datos abiertos** (*open data*) son plataformas gubernamentales o
    institucionales que publican conjuntos de datos de forma gratuita y con licencias
    que permiten su reutilización. Son una fuente valiosa tanto para práctica académica
    como para proyectos de analítica con impacto social.

    | Portal | Alcance | Ejemplos de datasets |
    |---|---|---|
    | [datos.gov.co](https://www.datos.gov.co/) | Colombia (nacional) | Presupuesto público, salud, educación, seguridad |
    | [DANE](https://www.dane.gov.co/) | Colombia (estadísticas oficiales) | Censo poblacional, PIB, encuestas de hogares |
    | [data.gov](https://www.data.gov/) | Estados Unidos | Clima, transporte, energía |
    | [EU Open Data Portal](https://data.europa.eu/) | Unión Europea | Economía, medio ambiente, movilidad |
    | [Banco Mundial (World Bank Open Data)](https://data.worldbank.org/) | Global | Indicadores de desarrollo por país |
    | [Google Dataset Search](https://datasetsearch.research.google.com/) | Global (buscador) | Metabuscador de datasets de múltiples fuentes |

    !!! note "Licencias y atribución"
        Al usar datos abiertos, revisa siempre la licencia asociada (por ejemplo,
        Creative Commons, Open Data Commons) y cita la fuente en tus visualizaciones
        publicadas. Muchas licencias exigen atribución explícita incluso para uso no
        comercial.

=== "2. Canales de publicación"

    Una vez construida una visualización, existen varios canales gratuitos o de bajo
    costo para publicarla y hacerla accesible al público:

    === "GitHub Pages"

        Servicio de hosting estático gratuito integrado en GitHub. Ideal para publicar
        sitios generados con MkDocs (como este mismo curso), notebooks convertidos a
        HTML, o gráficos exportados de Plotly/Bokeh embebidos en una página HTML.
        Se activa desde la configuración del repositorio (`Settings → Pages`) o
        mediante el comando `mkdocs gh-deploy`.

    === "Tableau Public"

        Versión gratuita de Tableau que permite publicar dashboards interactivos en la
        web, con la limitación de que los datos y visualizaciones son públicos y
        accesibles por cualquier persona. Es ampliamente usado en periodismo de datos y
        portafolios profesionales.

    === "Observable"

        Plataforma basada en JavaScript (creada por los autores de D3.js) para crear
        *notebooks* de visualización interactiva reactiva, con posibilidad de
        publicación y *forking* colaborativo (similar a un "Google Docs" para
        visualización de datos).

    === "Streamlit Community Cloud"

        Permite desplegar gratuitamente aplicaciones Streamlit directamente desde un
        repositorio de GitHub, ideal para prototipos de dashboards interactivos con
        Python sin necesidad de gestionar infraestructura.

    !!! tip "Buenas prácticas"
        Antes de publicar una visualización con datos sensibles (información
        personal, ubicaciones exactas, datos de salud), verifica que estén
        anonimizados o agregados a un nivel que impida la reidentificación de
        individuos, en línea con principios de protección de datos como el Habeas
        Data (Ley 1581 de 2012 en Colombia) o el RGPD europeo.

=== "3. Ejemplo: exportar a HTML"

    Una de las grandes ventajas de librerías como Plotly es que los gráficos se pueden
    exportar como archivos HTML autocontenibles (con el JavaScript embebido), listos
    para publicarse en cualquier servidor estático, incluyendo GitHub Pages.

    ```python
    """
    Ejemplo: Exportar un gráfico interactivo de Plotly a HTML autocontenible.
    Requiere: pandas, numpy, plotly

    Ejecución:
        python exportar_grafico_html.py

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
    # Salida esperada:
    # Se crea el archivo grafico_interactivo.html en el directorio actual. Al
    # abrirlo en un navegador, se muestra un gráfico de líneas interactivo (zoom,
    # pan, tooltips al pasar el cursor, y leyenda clickeable para mostrar/ocultar
    # países) que puede publicarse tal cual en GitHub Pages.
    ```

!!! example "Ejercicio propuesto"
    1. Genera tu propio dataset sintético (por ejemplo, precios de vivienda por
       ciudad a lo largo de 5 años) y exporta un gráfico interactivo de Plotly a
       HTML siguiendo el ejemplo anterior.
    2. Crea un repositorio de GitHub, sube el archivo HTML generado y publica un
       sitio con GitHub Pages apuntando a ese archivo. Documenta los pasos que
       seguiste.
    3. Investiga y describe (en un párrafo de 5-8 líneas) las diferencias entre
       publicar en Tableau Public y publicar un archivo HTML propio en GitHub
       Pages, en términos de control sobre los datos, costo y facilidad de uso.

## Referencias

- datos.gov.co — Portal de Datos Abiertos de Colombia:
  <https://www.datos.gov.co/>
- DANE — Departamento Administrativo Nacional de Estadística:
  <https://www.dane.gov.co/>
- Documentación de GitHub Pages: <https://docs.github.com/pages>
- Documentación de Tableau Public: <https://public.tableau.com/>
- Documentación de Observable: <https://observablehq.com/>
- Congreso de Colombia. (2012). Ley 1581 de 2012 — Protección de Datos
  Personales (Habeas Data).
