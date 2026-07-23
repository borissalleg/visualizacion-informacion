## Cuadros de mando (dashboards)

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/borissalleg/visualizacion-informacion/blob/main/examples/unidad-2/01_dashboard_ventas_streamlit.ipynb)

> ### Objetivos de aprendizaje
> Al finalizar este subtema, el estudiante será capaz de:
>
> - Definir qué es un cuadro de mando (dashboard) y diferenciarlo de un reporte
>   estático.
> - Clasificar los dashboards según su propósito: operacional, estratégico y
>   analítico.
> - Aplicar principios de jerarquía visual y patrones de lectura (F-pattern) al
>   diseño de un dashboard.
> - Construir un dashboard simple con Streamlit equivalente a uno diseñado en Power
>   BI.

=== "1. ¿Qué es un cuadro de mando?"

    Un **cuadro de mando** o **dashboard** es una herramienta de visualización que
    consolida y presenta, en una sola pantalla, los indicadores clave (KPIs) necesarios
    para monitorear el estado de un proceso, negocio u organización, con el objetivo de
    apoyar la toma de decisiones. A diferencia de un reporte estático, un dashboard
    suele actualizarse periódicamente y muchas veces incorpora interactividad (filtros,
    drill-down).

    **Tipos de dashboards**

    | Tipo | Propósito | Frecuencia de actualización | Audiencia típica | Ejemplo |
    |---|---|---|---|---|
    | **Operacional** | Monitoreo en tiempo real de procesos operativos | Segundos a minutos | Supervisores, equipos de operaciones | Panel de monitoreo de un call center (llamadas en cola, tiempo de espera) |
    | **Estratégico** | Seguimiento de objetivos de alto nivel a mediano/largo plazo | Diario, semanal, mensual | Directivos, junta directiva | Cuadro de mando integral (Balanced Scorecard) con metas anuales |
    | **Analítico** | Exploración profunda de datos para descubrir patrones y causas | Bajo demanda | Analistas de datos, científicos de datos | Dashboard interactivo de análisis de cohortes de usuarios |

    !!! note "Diferencia clave"
        Los dashboards operacionales priorizan la **inmediatez** (¿qué está pasando
        ahora mismo?), los estratégicos priorizan el **contexto histórico y las metas**
        (¿vamos bien respecto al objetivo anual?), y los analíticos priorizan la
        **flexibilidad exploratoria** (¿por qué está pasando esto?).

=== "2. Buenas prácticas de diseño"

    === "2.1 Jerarquía visual"

        La jerarquía visual organiza los elementos de un dashboard según su importancia
        relativa, guiando el recorrido visual del usuario. Se logra mediante:

        - **Tamaño**: los KPIs más importantes deben ocupar más espacio o usar tipografía
          más grande.
        - **Posición**: la información más relevante se ubica en la esquina superior
          izquierda (ver F-pattern) o en el centro superior.
        - **Color y contraste**: reservar colores saturados o de alerta (rojo, naranja)
          para llamar la atención sobre desviaciones críticas; usar tonos neutros para el
          resto.
        - **Agrupación (Gestalt)**: agrupar visualmente los indicadores relacionados
          (ej. todos los KPIs de "ventas" juntos, separados de los de "logística").

    === "2.2 Patrón de lectura en F"

        Estudios de *eye-tracking* (seguimiento ocular) muestran que, al escanear una
        pantalla con contenido denso, los usuarios occidentales (que leen de izquierda a
        derecha) siguen un patrón en forma de "F": primero una línea horizontal en la parte
        superior, luego otra línea horizontal más corta un poco más abajo, y finalmente un
        recorrido vertical por el lado izquierdo. Esto tiene implicaciones directas para el
        diseño de dashboards:

        - Coloca el KPI más crítico en la esquina superior izquierda.
        - Ubica los filtros y controles de navegación en la parte superior o en una barra
          lateral izquierda, donde el ojo los detecta primero.
        - No asumas que el usuario leerá todo el contenido de abajo a la derecha: la
          información menos crítica puede ubicarse ahí sin temor a que se pierda impacto.

        !!! tip "Buenas prácticas"
            - Limita el número de KPIs "por encima del scroll" a un máximo de 5-7 (ley de
              Miller sobre la capacidad de la memoria de trabajo).
            - Usa un máximo de 2-3 colores de énfasis; el resto de la paleta debe ser
              neutra.
            - Alinea los elementos en una cuadrícula (grid) consistente para reducir el
              "ruido visual" y facilitar el escaneo.
            - Incluye siempre el contexto temporal (rango de fechas de los datos
              mostrados) y la fecha/hora de la última actualización.

        !!! warning "Errores comunes"
            Saturar el dashboard con demasiados gráficos de tipos distintos ("dashboard
            zoológico") obliga al usuario a cambiar constantemente de "modo de lectura"
            (de un gráfico de líneas a uno de barras, a un mapa, a una tabla), aumentando
            la carga cognitiva. Prefiere la consistencia: usa el mismo tipo de gráfico para
            representar el mismo tipo de comparación en todo el dashboard.

=== "3. Ejemplo: Power BI vs. Streamlit"

    === "Power BI (paso a paso descrito)"

        Aunque este curso se enfoca en herramientas de código abierto, es común encontrar
        Power BI en entornos empresariales. A continuación se describe el flujo de trabajo
        típico para construir un dashboard estratégico de ventas:

        1. **Conectar la fuente de datos**: `Obtener datos → Excel/SQL Server/API` e
           importar la tabla de transacciones de ventas.
        2. **Modelar los datos**: en la vista de "Modelo", definir relaciones entre la
           tabla de hechos (`Ventas`) y las tablas de dimensión (`Productos`, `Clientes`,
           `Calendario`).
        3. **Crear medidas DAX**: por ejemplo,
           `Ventas Totales = SUM(Ventas[Monto])` y
           `Ventas YTD = TOTALYTD([Ventas Totales], Calendario[Fecha])`.
        4. **Diseñar el lienzo**: agregar una tarjeta (`Card`) para el KPI principal
           (Ventas Totales YTD), un gráfico de líneas para la tendencia mensual, un mapa
           coroplético para ventas por departamento, y una tabla de detalle filtrable.
        5. **Aplicar jerarquía visual**: ubicar la tarjeta de KPI principal en la esquina
           superior izquierda, con tipografía grande; los gráficos secundarios debajo o a
           la derecha.
        6. **Agregar interactividad**: insertar segmentadores (`slicers`) para año, región
           y línea de producto, habilitando *cross-filtering* entre visuales.
        7. **Publicar**: `Archivo → Publicar → Power BI Service`, y configurar la
           actualización programada de los datos (`Scheduled Refresh`).

    === "Equivalente en Python (Streamlit)"

        El siguiente ejemplo construye un dashboard estratégico de ventas equivalente al
        descrito en Power BI, usando datos sintéticos y Streamlit.

        ```python
        """
        Ejemplo: Dashboard estratégico de ventas con Streamlit.
        Requiere: streamlit, pandas, numpy, plotly

        Ejecución:
            streamlit run dashboard_ventas.py
        """
        import numpy as np
        import pandas as pd
        import plotly.express as px
        import streamlit as st

        st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

        # --- 1. Generación de datos sintéticos ---
        np.random.seed(3)
        fechas = pd.date_range("2025-01-01", "2025-12-31", freq="D")
        departamentos = ["Antioquia", "Bogotá D.C.", "Valle del Cauca", "Atlántico", "Santander"]
        lineas_producto = ["Electrónica", "Hogar", "Moda", "Alimentos"]

        df = pd.DataFrame({
            "fecha": np.random.choice(fechas, size=3000),
            "departamento": np.random.choice(departamentos, size=3000),
            "linea_producto": np.random.choice(lineas_producto, size=3000),
            "monto": np.random.gamma(shape=2.0, scale=80, size=3000).round(2),
        })
        df["mes"] = df["fecha"].dt.to_period("M").astype(str)

        # --- 2. Barra lateral: filtros (segmentadores, equivalentes a los slicers de Power BI) ---
        st.sidebar.header("Filtros")
        depto_sel = st.sidebar.multiselect("Departamento", departamentos, default=departamentos)
        linea_sel = st.sidebar.multiselect("Línea de producto", lineas_producto, default=lineas_producto)

        df_filtrado = df[df["departamento"].isin(depto_sel) & df["linea_producto"].isin(linea_sel)]

        # --- 3. KPI principal (tarjeta, esquina superior izquierda por jerarquía visual) ---
        st.title("📊 Dashboard estratégico de ventas — Año 2025")
        col1, col2, col3 = st.columns(3)
        col1.metric("Ventas totales (YTD)", f"${df_filtrado['monto'].sum():,.0f}")
        col2.metric("Ticket promedio", f"${df_filtrado['monto'].mean():,.2f}")
        col3.metric("Transacciones", f"{len(df_filtrado):,}")

        # --- 4. Gráfico de tendencia mensual ---
        tendencia = df_filtrado.groupby("mes")["monto"].sum().reset_index()
        fig_tendencia = px.line(tendencia, x="mes", y="monto", title="Tendencia mensual de ventas",
                                  markers=True)
        st.plotly_chart(fig_tendencia, use_container_width=True)

        # --- 5. Distribución por departamento y línea de producto ---
        col_a, col_b = st.columns(2)
        por_depto = df_filtrado.groupby("departamento")["monto"].sum().sort_values(ascending=False).reset_index()
        fig_depto = px.bar(por_depto, x="departamento", y="monto", title="Ventas por departamento")
        col_a.plotly_chart(fig_depto, use_container_width=True)

        por_linea = df_filtrado.groupby("linea_producto")["monto"].sum().reset_index()
        fig_linea = px.pie(por_linea, names="linea_producto", values="monto",
                             title="Participación por línea de producto")
        col_b.plotly_chart(fig_linea, use_container_width=True)

        # --- 6. Tabla de detalle filtrable ---
        with st.expander("Ver datos de detalle"):
            st.dataframe(df_filtrado.sort_values("fecha", ascending=False))

        # Salida esperada:
        # Un dashboard web con tarjetas de KPI en la parte superior, un gráfico de
        # tendencia mensual, dos gráficos de distribución (barras y circular) y una
        # tabla de detalle colapsable, todo filtrable desde la barra lateral por
        # departamento y línea de producto — replicando la experiencia de un dashboard
        # de Power BI usando componentes de código abierto.
        ```

!!! example "Ejercicio propuesto"
    1. Extiende el dashboard de Streamlit anterior agregando un filtro de rango de
       fechas (`st.date_input` o `st.slider` con fechas).
    2. Agrega un indicador de variación porcentual respecto al mes anterior en la
       tarjeta de "Ventas totales" (usa el parámetro `delta` de `st.metric`).
    3. Diseña en papel (o en una herramienta de wireframing) la disposición de un
       dashboard **operacional** para un centro de distribución logística,
       aplicando el patrón F: identifica qué KPI iría en la esquina superior
       izquierda y justifica tu elección.

## Referencias

- Few, S. (2006). *Information Dashboard Design: The Effective Visual
  Communication of Data*. O'Reilly Media.
- Kaplan, R. S., & Norton, D. P. (1996). *The Balanced Scorecard: Translating
  Strategy into Action*. Harvard Business School Press.
- Nielsen Norman Group. (2006). *F-Shaped Pattern for Reading Web Content*.
  <https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/>
- Documentación oficial de Power BI: <https://learn.microsoft.com/power-bi/>
- Documentación oficial de Streamlit: <https://docs.streamlit.io/>
