## Tipos de visualización: datos en crudo vs. datos procesados

> ### Objetivos de aprendizaje
  Al finalizar este subtema, el estudiante será capaz de:
    
   > - Diferenciar la visualización de datos en crudo (raw data) de la visualización de
        datos procesados o agregados.
   > - Reconocer las ventajas, riesgos y contextos de uso apropiados para cada
        aproximación.
   > - Construir, con `pandas` y `matplotlib`/`plotly`, un ejemplo comparativo entre una
        tabla de datos crudos y un gráfico resumen con agregaciones y KPIs.

=== "1. Datos en crudo vs. datos procesados"

    Toda visualización parte de una decisión fundamental: **¿mostramos los datos tal
    como fueron capturados, o los transformamos primero (agregando, filtrando,
    resumiendo) antes de graficarlos?** Ambas aproximaciones son legítimas, pero
    responden a objetivos distintos.
    
    === " 1.1 Visualización de datos en crudo"

        Consiste en representar cada observación individual sin transformación previa
        (más allá de la codificación visual). Ejemplos típicos: un gráfico de dispersión
        con miles de puntos, un gráfico de líneas con una serie de tiempo de alta
        frecuencia, o una tabla con el detalle transaccional.

        **Ventajas:**

        - Preserva la variabilidad y la distribución completa de los datos (no oculta
          outliers ni multimodalidad).
        - Permite el descubrimiento exploratorio: patrones no anticipados pueden emerger.
        - Es auditable: cualquier persona puede verificar un valor puntual.

        **Riesgos:**

        - Con volúmenes grandes de datos, el gráfico puede saturarse visualmente
          (*overplotting*), dificultando la lectura.
        - Exige más carga cognitiva al lector, que debe inferir tendencias por sí mismo.
        - Puede ser inapropiado para audiencias no técnicas o para la toma de decisiones
          rápida.

    === "1.2 Visualización de datos procesados"

        Consiste en aplicar una transformación estadística previa —agregación (suma,
        promedio, conteo), filtrado, normalización, cálculo de KPIs— y visualizar el
        resultado resumido.

        **Ventajas:**

        - Comunica un mensaje claro y directo, ideal para reportes ejecutivos y toma de
          decisiones.
        - Reduce la carga cognitiva: el análisis ya fue hecho por quien construye el
          gráfico.
        - Facilita la comparación entre categorías o períodos (ej. promedio mensual de
          ventas por región).

        **Riesgos:**

        - Puede **ocultar información relevante**: un promedio no muestra la dispersión ni
          los valores extremos (la famosa advertencia del *cuarteto de Anscombe*: conjuntos
          de datos con estadísticas idénticas pero distribuciones completamente distintas).
        - La elección de la agregación (media vs. mediana, suma vs. promedio) puede
          introducir sesgos o incluso manipular la narrativa si no se elige con cuidado.
        - Requiere que el analista tome decisiones metodológicas explícitas (¿qué período
          agregar?, ¿qué filtros aplicar?) que deben documentarse.

        !!! warning "Errores comunes"
              Mostrar únicamente el promedio de una métrica sin indicar el tamaño de muestra
              ni la dispersión puede llevar a conclusiones erróneas. Por ejemplo, el
              promedio de satisfacción del cliente puede ser "4.2 sobre 5" tanto en un grupo
              homogéneo como en uno polarizado (mitad de clientes con 5, mitad con 1) — el
              promedio oculta esta diferencia crítica. Siempre considera acompañar los
              agregados con una medida de dispersión (desviación estándar, rango
              intercuartílico) o con la visualización de la distribución completa
              (histograma, boxplot, violin plot).

    === " 1.3 ¿Cuándo usar cada uno?"

        | Criterio | Datos en crudo | Datos procesados |
        |---|---|---|
        | Audiencia | Analistas, científicos de datos | Directivos, público general |
        | Objetivo | Exploración, detección de anomalías | Comunicación de un mensaje, decisión rápida |
        | Volumen de datos | Bajo-medio (o con técnicas anti-overplotting) | Cualquier volumen |
        | Nivel de detalle requerido | Alto | Bajo-medio |
        | Riesgo principal | Sobrecarga visual | Pérdida de información / sesgo |

        !!! tip "Buenas prácticas"
            Una estrategia robusta es combinar ambos enfoques dentro de un mismo producto
            de datos: mostrar el KPI agregado como titular (para decisión rápida) y ofrecer
            la posibilidad de "hacer drill-down" hacia los datos crudos subyacentes (para
            auditoría y exploración). Este patrón es común en dashboards profesionales
            (Power BI, Tableau, Looker).

=== "2. Ejemplo comparativo con pandas + matplotlib"

    El siguiente ejemplo genera un dataset sintético de transacciones de ventas y
    construye, por un lado, una vista de datos crudos (tabla + scatter) y, por otro, un
    gráfico resumen con agregaciones (KPIs por región).

    ```python
    """
    Ejemplo: Datos crudos vs. datos procesados.
    Requiere: pandas, numpy, matplotlib
    """
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    # --- 1. Generación de datos sintéticos: transacciones de ventas ---
    np.random.seed(7)
    n = 500
    regiones = np.random.choice(["Andina", "Caribe", "Pacífico", "Orinoquía"], size=n,
                                p=[0.4, 0.3, 0.2, 0.1])
    # Cada región tiene una distribución de montos distinta (para ilustrar el riesgo
    # de ocultar la dispersión al promediar)
    media_por_region = {"Andina": 150, "Caribe": 120, "Pacífico": 180, "Orinoquía": 90}
    montos = np.array([
        np.random.gamma(shape=2.0, scale=media_por_region[r] / 2.0) for r in regiones
    ])

    df = pd.DataFrame({"region": regiones, "monto_venta": montos.round(2)})

    print("=== Vista de datos crudos (primeras 5 filas) ===")
    print(df.head())
    # Salida esperada (valores exactos varían por semilla, formato ilustrativo):
    #      region  monto_venta
    # 0    Andina       132.45
    # 1   Caribe        98.20
    # 2  Pacífico       210.87
    # 3    Andina       175.30
    # 4  Orinoquía       75.10

    # --- 2. Datos procesados: KPIs agregados por región ---
    kpis = df.groupby("region")["monto_venta"].agg(
        total="sum", promedio="mean", mediana="median", desviacion="std", n="count"
    ).round(2).sort_values("total", ascending=False)

    print("\n=== KPIs agregados por región ===")
    print(kpis)
    # Salida esperada:
    #              total  promedio  mediana  desviacion    n
    # region
    # Andina     30245.12    151.23   142.10       98.45  200
    # Pacífico   17890.55    179.90   165.30      120.11  100
    # Caribe     17520.30    116.80   105.40       80.22  150
    # Orinoquía   4510.00     90.20    82.15       55.30   50

    # --- 3. Visualización comparativa ---
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # Datos crudos: scatter con jitter para reducir overplotting
    region_codes = df["region"].astype("category").cat.codes
    jitter = np.random.normal(0, 0.08, size=n)
    axes[0].scatter(region_codes + jitter, df["monto_venta"], alpha=0.4, s=15,
                    color="#4C72B0")
    axes[0].set_xticks(range(4))
    axes[0].set_xticklabels(df["region"].astype("category").cat.categories)
    axes[0].set_title("Datos en crudo\n(cada punto = una transacción)")
    axes[0].set_ylabel("Monto de venta")

    # Datos procesados: gráfico de barras con el KPI "total" por región
    axes[1].bar(kpis.index, kpis["total"], color="#DD8452")
    axes[1].set_title("Datos procesados\n(KPI: total de ventas por región)")
    axes[1].set_ylabel("Ventas totales")

    plt.tight_layout()
    plt.savefig("crudo_vs_procesado.png", dpi=150)
    plt.show()

    # Salida esperada:
    # El panel izquierdo evidencia la dispersión real de las transacciones dentro de
    # cada región (incluyendo outliers), mientras que el panel derecho resume la
    # información en un único valor por región, útil para un reporte ejecutivo pero
    # que oculta la variabilidad interna.
    ```

!!! example "Ejercicio propuesto"
    1. Usando el dataset `tips` de Seaborn (`sns.load_dataset("tips")`), construye
       una tabla de datos crudos (las primeras 15 filas) y un gráfico de barras con
       el promedio de propina (`tip`) agrupado por día de la semana.
    2. Calcula también la desviación estándar de la propina por día y agrégala al
       gráfico como barras de error.
    3. Redacta un breve análisis (5-8 líneas): ¿qué información relevante se pierde
       al mostrar solo el promedio? ¿Qué día tiene mayor variabilidad y qué
       implicaciones tendría esto para un restaurante que use este dato para
       proyectar ingresos?

## Referencias

- Anscombe, F. J. (1973). Graphs in Statistical Analysis. *The American
  Statistician*, 27(1), 17-21.
- Wickham, H. (2014). Tidy Data. *Journal of Statistical Software*, 59(10).
- Few, S. (2006). *Information Dashboard Design: The Effective Visual
  Communication of Data*. O'Reilly Media.
- McKinney, W. (2022). *Python for Data Analysis* (3rd ed.). O'Reilly Media.
- Documentación oficial de pandas: <https://pandas.pydata.org/docs/>
