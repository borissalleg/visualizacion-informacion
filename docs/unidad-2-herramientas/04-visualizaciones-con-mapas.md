## Visualizaciones con mapas

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/borissalleg/visualizacion-informacion/blob/main/examples/unidad-2/04_mapa_marcadores_folium.ipynb)

> ### Objetivos de aprendizaje
> Al finalizar este subtema, el estudiante será capaz de:
>
> - Explicar los componentes básicos de un mapa temático (mapa base, marcadores,
>   capas).
> - Diferenciar las opciones de mapas base disponibles en Folium y Plotly.
> - Construir un mapa interactivo con marcadores a partir de un archivo CSV de
>   coordenadas.

=== "1. Introducción a los mapas temáticos"

    Un **mapa temático** representa la distribución espacial de una o más variables
    sobre una base geográfica, a diferencia de un mapa de referencia (que solo muestra
    límites administrativos, calles o accidentes geográficos). En Python, las dos
    librerías más usadas para construir mapas interactivos son:

    - **Folium**: envuelve la librería JavaScript [Leaflet.js](https://leafletjs.com/)
      y genera mapas interactivos como archivos HTML, ideales para exploración rápida y
      publicación web.
    - **Plotly** (`plotly.express` con `px.scatter_mapbox` / `px.choropleth_mapbox` o
      los nuevos `px.scatter_map` / `px.choropleth_map`): se integra bien con
      dashboards Plotly/Dash y permite combinar mapas con otros gráficos en una misma
      interfaz.

    **Componentes de un mapa interactivo**

    - **Mapa base (`tiles`)**: la capa de fondo (calles, satélite, relieve). Folium
      incluye proveedores como `OpenStreetMap`, `CartoDB positron` (minimalista, ideal
      para no competir visualmente con los datos) y `Stamen Terrain`.
    - **Marcadores (`markers`)**: puntos que representan ubicaciones específicas
      (ej. sucursales, eventos, estaciones). Pueden personalizarse con íconos, colores
      y popups de información.
    - **Capas (`layers`)**: agrupaciones de elementos que pueden activarse/desactivarse
      de forma independiente (ej. una capa de "sucursales" y otra de "clientes"),
      gestionadas mediante `folium.LayerControl()`.
    - **Clústeres de marcadores (`MarkerCluster`)**: agrupan visualmente marcadores
      cercanos cuando hay demasiados puntos, evitando el *overplotting* y mejorando el
      rendimiento del mapa.

    !!! note "Elección del mapa base"
        Para mapas temáticos donde los datos son el protagonista (por ejemplo, un mapa
        de calor o un coroplético), se recomienda un mapa base minimalista como
        `CartoDB positron`, que reduce el ruido visual de calles y etiquetas,
        permitiendo que los colores y marcadores de los datos resalten (aplicando el
        principio de data-ink ratio visto en la Unidad 1).

=== "2. Ejemplo: mapa con marcadores desde CSV"

    En este ejemplo se construye un mapa interactivo con Folium a partir de un CSV
    sintético de sucursales de una cadena de tiendas en Colombia, incluyendo popups
    informativos y agrupación de marcadores.

    ```python
    """
    Ejemplo: Mapa interactivo con marcadores desde un CSV de coordenadas.
    Requiere: folium, pandas

    Ejecución:
        python mapa_marcadores_folium.py

    Genera un archivo "mapa_sucursales.html" que puede abrirse en cualquier
    navegador o publicarse como página estática (ver Unidad 2, subtema 2).
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
        tiles="CartoDB positron",  # mapa base minimalista (alto data-ink ratio)
    )

    # --- 3. Agrupador de marcadores (evita saturación visual con muchos puntos) ---
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

    # --- 5. Control de capas (permite activar/desactivar el clúster de sucursales) ---
    folium.LayerControl().add_to(mapa)

    # --- 6. Guardar como HTML ---
    mapa.save("mapa_sucursales.html")
    print("Mapa guardado en 'mapa_sucursales.html'")

    # Salida esperada:
    # Un archivo HTML con un mapa centrado en Colombia, mostrando 8 marcadores
    # (uno por sucursal) con ícono de carrito de compras: verde para sucursales
    # con ventas >= 70,000 y naranja para las demás. Al hacer clic sobre un
    # marcador se despliega un popup con el nombre, ciudad y ventas mensuales;
    # al pasar el cursor se muestra un tooltip con el nombre de la sucursal.
    ```

    !!! tip "Buenas prácticas"
        - Usa `MarkerCluster` cuando tengas más de 20-30 marcadores, para evitar que
          se superpongan y se vuelvan ilegibles al alejar el zoom.
        - Codifica información adicional mediante el color o ícono del marcador
          (como en el ejemplo, verde/naranja según ventas), aprovechando el canal de
          "similitud" de Gestalt para que el usuario agrupe visualmente los
          marcadores por categoría sin necesidad de leer cada popup.
        - Siempre incluye un popup o tooltip con el detalle exacto: el mapa da
          contexto espacial, pero los valores precisos deben estar accesibles bajo
          demanda (principio de *details-on-demand* de Shneiderman, visto en la
          Unidad 1).

    !!! warning "Errores comunes"
        Usar demasiados colores o íconos distintos en un mismo mapa sin una leyenda
        clara genera confusión. Si necesitas codificar más de 4-5 categorías por
        color, considera usar un mapa coroplético (Unidad 3) o dividir la información
        en capas activables por separado con `LayerControl`.

!!! example "Ejercicio propuesto"
    1. Amplía el CSV sintético del ejemplo con al menos 15 sucursales adicionales
       distribuidas en más ciudades de Colombia.
    2. Agrega una segunda capa al mapa (por ejemplo, "Bodegas" o "Centros de
       distribución") con un ícono y color distintos, y actívala/desactívala usando
       `folium.LayerControl()`.
    3. Investiga cómo agregar un mapa de calor (`folium.plugins.HeatMap`) sobre
       las mismas coordenadas y compáralo visualmente con el mapa de marcadores:
       ¿en qué escenario preferirías uno sobre el otro? (Este concepto se
       profundiza en la Unidad 3, subtema de mapas de densidad).

## Referencias

- Documentación oficial de Folium: <https://python-visualization.github.io/folium/>
- Documentación de Leaflet.js: <https://leafletjs.com/>
- Documentación de Plotly Maps: <https://plotly.com/python/maps/>
- CartoDB Basemaps: <https://carto.com/basemaps>
