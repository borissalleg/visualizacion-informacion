## Visualización dinámica de datos

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/borissalleg/visualizacion-informacion/blob/main/examples/unidad-1/04_dashboard_tiempo_real.ipynb)

> ### Objetivos de aprendizaje
> Al finalizar este subtema, el estudiante será capaz de:
>
> - Explicar el concepto de interactividad en visualización de datos y sus niveles
>   (filtrado, detalle bajo demanda, coordinación entre vistas).
> - Comprender los fundamentos del procesamiento y visualización de datos en
>   streaming (tiempo real o cuasi real).
> - Construir un dashboard simple con actualización periódica usando Streamlit,
>   alimentado por datos simulados.

=== "1. Interactividad en la visualización"

    Una visualización **estática** (una imagen PNG, un gráfico impreso) transmite un
    mensaje fijo. Una visualización **dinámica o interactiva** permite al usuario
    manipular la representación para explorar distintas facetas de los datos sin
    necesidad de generar un nuevo gráfico desde cero. Ben Shneiderman resumió el
    principio rector de la interactividad en su célebre mantra de búsqueda visual:

    > *"Overview first, zoom and filter, then details-on-demand."*
    > (Primero una vista general, luego acercar y filtrar, y finalmente detalles bajo
    > demanda.)

    Los mecanismos de interactividad más comunes son:

    - **Filtrado (`filtering`)**: el usuario selecciona un subconjunto de datos
      (ej. un rango de fechas, una categoría) y el gráfico se actualiza en
      consecuencia.
    - **Zoom y paneo (`zoom & pan`)**: permite acercarse a una región específica de
      interés sin perder el contexto general.
    - **Detalles bajo demanda (`details-on-demand`)**: tooltips o paneles que muestran
      información adicional al pasar el cursor sobre una marca de datos.
    - **Coordinación entre vistas (`brushing & linking`)**: seleccionar datos en un
      gráfico resalta automáticamente los datos correspondientes en otros gráficos del
      mismo dashboard.
    - **Parámetros configurables por el usuario**: sliders, dropdowns o campos de
      entrada que modifican el cálculo subyacente (ej. cambiar el tipo de agregación).

    !!! note "Interactividad vs. animación"
        No hay que confundir interactividad con animación. Una animación (por ejemplo,
        un GIF que muestra la evolución del PIB por país a través del tiempo) es
        dinámica pero no necesariamente interactiva: el usuario no tiene control sobre
        ella. Una visualización interactiva, en cambio, responde a las acciones del
        usuario (clics, hover, selección).

=== "2. Streaming y tiempo real"

    === "2.1 Streaming de datos"

        Cuando los datos se generan continuamente —sensores IoT, transacciones
        financieras, logs de servidores, redes sociales— la visualización debe
        actualizarse periódicamente para reflejar el estado más reciente. Esto introduce
        retos específicos:

        - **Frecuencia de actualización**: debe balancear la "frescura" de los datos con el
          costo computacional y de red de refrescar constantemente. Un dashboard operativo
          puede actualizarse cada segundo; un reporte gerencial puede bastar con
          actualizarse cada hora.
        - **Ventanas deslizantes (`sliding windows`)**: en lugar de acumular todo el
          histórico, muchas visualizaciones en tiempo real muestran solo los últimos *N*
          minutos u observaciones, para mantener el gráfico legible y con buen desempeño.
        - **Agregación incremental**: recalcular agregaciones (promedios, sumas) de forma
          incremental en lugar de recorrer todo el histórico en cada actualización, para
          garantizar baja latencia.
        - **Gestión del layout**: los ejes deben ajustarse dinámicamente (o fijarse
          deliberadamente) para que la llegada de nuevos datos no distorsione la
          interpretación visual de un momento a otro.

        !!! warning "Errores comunes"
            Un error frecuente es reescalar automáticamente el eje Y en cada actualización
            de un gráfico en tiempo real. Esto puede hacer parecer que hay cambios
            drásticos en la tendencia cuando en realidad solo cambió el rango del eje. Es
            recomendable fijar límites del eje basados en el rango esperado del fenómeno, o
            al menos suavizar los cambios de escala.

    === "2.2 Arquitecturas típicas"

        En un flujo de datos en tiempo real, la visualización suele ser la última capa de
        una arquitectura como:

        ```text
        Fuente de datos → Ingesta (Kafka/MQTT/API) → Procesamiento (streaming) → Almacenamiento
                                                                                      ↓
                                                                    Capa de visualización (dashboard)
        ```

        Herramientas como **Plotly Dash** y **Streamlit** permiten construir esta capa de
        visualización rápidamente en Python, con soporte para actualización periódica
        (*polling*) o mediante *callbacks* reactivos.

=== "3. Ejemplo: dashboard con Streamlit"

    El siguiente ejemplo simula un sensor de temperatura y humedad que emite lecturas
    cada segundo, y construye un dashboard que se actualiza automáticamente mostrando
    las últimas *N* lecturas (ventana deslizante) y KPIs en tiempo real.

    ```python
    """
    Ejemplo: Dashboard con actualización periódica usando Streamlit.
    Requiere: streamlit, pandas, numpy

    Ejecución:
        streamlit run dashboard_tiempo_real.py

    El script simula la llegada de datos de un sensor IoT (temperatura y humedad)
    y actualiza el dashboard cada segundo, manteniendo una ventana deslizante de
    las últimas 50 lecturas.
    """
    import time
    from collections import deque

    import numpy as np
    import pandas as pd
    import streamlit as st

    st.set_page_config(page_title="Sensor IoT en tiempo real", layout="wide")
    st.title("📡 Dashboard de sensor IoT — actualización en tiempo real")

    VENTANA = 50  # número máximo de lecturas a mostrar (sliding window)
    INTERVALO_SEGUNDOS = 1

    # --- Estado de la sesión: buffers para la ventana deslizante ---
    if "tiempos" not in st.session_state:
        st.session_state.tiempos = deque(maxlen=VENTANA)
        st.session_state.temperaturas = deque(maxlen=VENTANA)
        st.session_state.humedades = deque(maxlen=VENTANA)
        st.session_state.tick = 0


    def simular_lectura_sensor(tick: int) -> tuple[float, float]:
        """Genera una lectura sintética de temperatura (°C) y humedad (%)."""
        temperatura = 22 + 3 * np.sin(tick / 10) + np.random.normal(0, 0.4)
        humedad = 55 + 10 * np.cos(tick / 15) + np.random.normal(0, 1.2)
        return round(temperatura, 2), round(humedad, 2)


    # --- Placeholder que se redibuja en cada iteración ---
    placeholder = st.empty()

    # NOTA: en un entorno real, este bucle se sustituiría por una suscripción a un
    # tópico de Kafka/MQTT o por polling a una API. Aquí se simula con un bucle
    # controlado que se detiene tras 200 iteraciones para no bloquear el proceso
    # indefinidamente en un entorno de demostración.
    for _ in range(200):
        st.session_state.tick += 1
        temp, hum = simular_lectura_sensor(st.session_state.tick)
        st.session_state.tiempos.append(st.session_state.tick)
        st.session_state.temperaturas.append(temp)
        st.session_state.humedades.append(hum)

        df = pd.DataFrame({
            "tick": list(st.session_state.tiempos),
            "temperatura_C": list(st.session_state.temperaturas),
            "humedad_%": list(st.session_state.humedades),
        })

        with placeholder.container():
            col1, col2, col3 = st.columns(3)
            col1.metric("Temperatura actual (°C)", f"{temp:.1f}",
                        f"{temp - df['temperatura_C'].iloc[-2]:.1f}" if len(df) > 1 else None)
            col2.metric("Humedad actual (%)", f"{hum:.1f}")
            col3.metric("Lecturas en ventana", len(df))

            st.line_chart(df.set_index("tick")[["temperatura_C"]])
            st.line_chart(df.set_index("tick")[["humedad_%"]])

        time.sleep(INTERVALO_SEGUNDOS)

    # Salida esperada:
    # Al ejecutar `streamlit run dashboard_tiempo_real.py`, se abre una pestaña del
    # navegador con tres tarjetas de KPI (temperatura actual, humedad actual y número
    # de lecturas en la ventana) y dos gráficos de línea que se actualizan cada
    # segundo mostrando la ventana deslizante de las últimas 50 lecturas simuladas.
    ```

    !!! tip "Buenas prácticas"
        - Usa ventanas deslizantes (`deque(maxlen=N)` o equivalentes) para evitar que
          el consumo de memoria crezca indefinidamente en aplicaciones de larga
          duración.
        - Separa claramente la lógica de "producción" de datos (el simulador o
          conexión real al stream) de la lógica de "presentación" (el dashboard), para
          poder testear ambas por separado.
        - En producción, evita bucles bloqueantes como el del ejemplo: usa
          `st.fragment` con `run_every` (Streamlit) o `dcc.Interval` (Dash) para
          actualizaciones periódicas no bloqueantes.

!!! example "Ejercicio propuesto"
    1. Modifica el ejemplo anterior para simular tres sensores ubicados en
       diferentes salas de un edificio, cada uno con su propia línea de tendencia
       de temperatura.
    2. Agrega un control interactivo (`st.slider`) que permita al usuario ajustar
       el tamaño de la ventana deslizante (por ejemplo, entre 20 y 200 lecturas) y
       observa cómo cambia la legibilidad del gráfico.
    3. Agrega una alerta visual (`st.warning`) que se dispare cuando la temperatura
       simulada supere un umbral configurable por el usuario.

## Referencias

- Shneiderman, B. (1996). The Eyes Have It: A Task by Data Type Taxonomy for
  Information Visualizations. *Proceedings of the IEEE Symposium on Visual
  Languages*.
- Heer, J., & Shneiderman, B. (2012). Interactive Dynamics for Visual Analysis.
  *Communications of the ACM*, 55(4), 45-54.
- Documentación oficial de Streamlit: <https://docs.streamlit.io/>
- Documentación oficial de Plotly Dash: <https://dash.plotly.com/>
- Akidau, T., Chernyak, S., & Lax, R. (2018). *Streaming Systems*. O'Reilly Media.
