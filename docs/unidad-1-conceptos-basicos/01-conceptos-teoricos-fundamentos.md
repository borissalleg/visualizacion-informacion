## Conceptos teóricos y fundamentos

**Ejemplo 1:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/borissalleg/visualizacion-informacion/blob/main/examples/unidad-1/01_comparacion_canales_visuales.ipynb)
&nbsp; **Ejemplo 2:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/borissalleg/visualizacion-informacion/blob/main/examples/unidad-1/02_data_ink_ratio.ipynb)

> ### Objetivos de aprendizaje
> Al finalizar este subtema, el estudiante será capaz de:
>
> - Definir qué es la visualización de información y diferenciarla de la infografía y
>   el arte de datos.
> - Describir brevemente la evolución histórica de la disciplina.
> - Explicar los principios de la psicología de la Gestalt aplicados al diseño visual.
> - Aplicar la jerarquía de canales visuales de Cleveland & McGill para elegir la
>   codificación visual más precisa según el tipo de dato.
> - Identificar prácticas de diseño que reducen la efectividad de una visualización
>   (chartjunk) y aplicar el principio de data-ink ratio de Edward Tufte.

=== "1. ¿Qué es la visualización de información?"

    La **visualización de información** es la representación gráfica de datos
    abstractos —numéricos o categóricos— con el propósito de amplificar la cognición
    humana: permitir que las personas detecten patrones, tendencias, anomalías y
    relaciones que serían difíciles de identificar mirando únicamente tablas de números.
    A diferencia de la visualización científica (que representa fenómenos con una
    correspondencia espacial física directa, como un escáner médico o una simulación de
    fluidos), la visualización de información trabaja con datos que **no tienen una
    representación espacial inherente** —ventas, encuestas, redes sociales, texto—, por
    lo que el diseñador debe *inventar* un mapeo visual (posición, color, forma) que
    sea comprensible e intuitivo.

    Es fundamental distinguir tres disciplinas que suelen confundirse:

    | Disciplina | Objetivo principal | Prioridad | Ejemplo típico |
    |---|---|---|---|
    | **Visualización de información** | Análisis y descubrimiento de patrones en los datos | Precisión y exactitud sobre estética | Un gráfico de dispersión en un notebook de análisis |
    | **Infografía** | Comunicar una narrativa o mensaje concreto a una audiencia general | Claridad narrativa y diseño gráfico | Una pieza editorial en un periódico |
    | **Arte de datos (data art)** | Provocar una reacción estética o emocional | Estética y expresión sobre precisión | Instalaciones generativas basadas en datos |

    Las tres pueden compartir los mismos datos de origen, pero difieren en su
    propósito: mientras que la visualización de información prioriza que el lector
    pueda **leer valores con precisión**, la infografía puede sacrificar algo de
    precisión para ganar impacto comunicativo, y el arte de datos puede prescindir por
    completo de la legibilidad exacta en favor de la experiencia estética.

    **Breve historia**

    La disciplina tiene antecedentes que se remontan a los mapas y diagramas del siglo
    XVIII. Algunos hitos clave:

    - **William Playfair** (1786) inventó el gráfico de líneas, de barras y el gráfico
      circular (*pie chart*) en su *Commercial and Political Atlas*.
    - **Charles Joseph Minard** (1869) creó el célebre mapa de la campaña de Napoleón en
      Rusia, considerado uno de los mejores gráficos estadísticos jamás realizados por
      combinar seis variables (tamaño del ejército, ubicación geográfica, dirección,
      temperatura y tiempo) en una sola imagen.
    - **John Tukey** (décadas de 1960-1970) impulsó el *Exploratory Data Analysis*
      (EDA), sentando las bases estadísticas de la visualización exploratoria moderna.
    - **Edward Tufte** (desde 1983, con *The Visual Display of Quantitative
      Information*) formalizó principios de diseño como el *data-ink ratio* y acuñó el
      término *chartjunk*.
    - **Jacques Bertin** (1967, *Sémiologie Graphique*) sistematizó las variables
      visuales (posición, tamaño, forma, valor, color, orientación, textura) que luego
      retomarían Cleveland & McGill.
    - La era digital (D3.js, Tableau, Power BI, y las librerías modernas de Python)
      democratizó la creación de visualizaciones interactivas a gran escala.

=== "2. Principios de percepción visual"

    === "2.1 Psicología de la Gestalt"

        La Gestalt es una corriente de la psicología que estudia cómo el cerebro humano
        organiza los elementos visuales en totalidades (*"el todo es más que la suma de sus
        partes"*). Sus principios más relevantes para el diseño de visualizaciones son:

        - **Proximidad**: los elementos cercanos entre sí se perciben como un grupo. Se
          usa para agrupar puntos de una misma categoría en un gráfico de dispersión sin
          necesidad de encerrarlos en un recuadro.
        - **Similitud**: elementos con el mismo color, forma o tamaño se perciben como
          pertenecientes al mismo grupo, incluso si están distantes. Es la base de la
          codificación por color en leyendas.
        - **Continuidad**: el ojo sigue líneas y curvas suaves antes que trazos abruptos.
          Por eso una serie de tiempo se lee más fácilmente como una línea continua que
          como puntos aislados.
        - **Cierre**: el cerebro completa formas incompletas. Permite simplificar
          gráficos (por ejemplo, un gráfico de radar) sin necesidad de dibujar todos los
          contornos.
        - **Figura-fondo**: distinguimos automáticamente un objeto (figura) de su entorno
          (fondo). Un buen contraste entre las marcas de datos y el fondo del gráfico
          mejora la legibilidad.

        !!! note "Aplicación práctica"
            Cuando diseñes un gráfico, pregúntate: *¿qué le pediría a un lector que agrupara
            mentalmente?* Si la respuesta requiere esfuerzo consciente, probablemente el
            principio de Gestalt correspondiente no se está aplicando correctamente (por
            ejemplo, colores demasiado similares entre categorías distintas).

    === "2.2 Canales visuales de Cleveland & McGill"

        En 1984, William Cleveland y Robert McGill publicaron un estudio experimental que
        ordenó los **canales de codificación visual** (las formas en que un valor numérico
        puede representarse gráficamente) según la precisión con la que el ojo humano puede
        decodificarlos. De mayor a menor precisión:

        1. **Posición en una escala común** (ej. un gráfico de barras con eje compartido)
        2. **Posición en escalas no alineadas** (ej. paneles pequeños múltiples)
        3. **Longitud** (ej. la altura de una barra)
        4. **Pendiente / ángulo** (ej. gráficos circulares o de pastel)
        5. **Área** (ej. burbujas en un scatter plot)
        6. **Volumen / Color (saturación)**
        7. **Color (matiz o tono)**

        !!! warning "Errores comunes"
            El **gráfico circular (pie chart)** utiliza el canal de *ángulo*, que se ubica
            en una posición intermedia-baja de la jerarquía de precisión. Por eso, cuando
            se necesita comparar valores con precisión (por ejemplo, participación de
            mercado de 5 competidores similares), un gráfico de barras (canal de
            *posición/longitud*) casi siempre comunica mejor que un gráfico circular.

    === "2.3 Chartjunk y data-ink ratio"

        Edward Tufte definió el **data-ink ratio** como:

        $$
        \text{data-ink ratio} = \frac{\text{tinta usada para representar datos}}{\text{tinta total impresa en el gráfico}}
        $$

        Un gráfico eficiente maximiza esta razón, eliminando elementos decorativos que no
        aportan información: fondos con textura, líneas de cuadrícula excesivas, efectos 3D
        en gráficos 2D, sombras, bordes duplicados, etc. A este exceso de elementos no
        informativos Tufte lo llamó **chartjunk**.

        !!! tip "Buenas prácticas"
            - Elimina bordes y fondos innecesarios en los gráficos.
            - Evita el efecto 3D en gráficos de barras o circulares: distorsiona la
              percepción de área y ángulo sin aportar información adicional.
            - Usa líneas de cuadrícula tenues (gris claro) solo como referencia, nunca como
              protagonistas visuales.
            - Etiqueta directamente las series cuando sea posible, en lugar de depender
              únicamente de una leyenda distante.

=== "3. Ejemplos prácticos en Python"

    === "Ejemplo 1 — Canales visuales"

        Este ejemplo genera un gráfico de barras y un gráfico circular con los mismos datos
        sintéticos, para evidenciar por qué el canal de posición/longitud permite una
        comparación más precisa que el canal de ángulo.

        ```python
        """
        Ejemplo 1: Comparación de canales visuales — posición vs. ángulo.
        Requiere: matplotlib
        """
        import matplotlib.pyplot as plt

        # Datos sintéticos: participación de mercado de 5 marcas (%)
        marcas = ["Marca A", "Marca B", "Marca C", "Marca D", "Marca E"]
        participacion = [23, 19, 21, 18, 19]  # valores intencionalmente similares

        fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

        # --- Gráfico circular (canal: ángulo) ---
        axes[0].pie(participacion, labels=marcas, autopct="%1.0f%%", startangle=90)
        axes[0].set_title("Gráfico circular\n(canal: ángulo)")

        # --- Gráfico de barras (canal: posición/longitud) ---
        axes[1].bar(marcas, participacion, color="#4C72B0")
        axes[1].set_title("Gráfico de barras\n(canal: posición/longitud)")
        axes[1].set_ylabel("Participación de mercado (%)")
        axes[1].set_ylim(0, 30)
        for i, v in enumerate(participacion):
            axes[1].text(i, v + 0.5, str(v), ha="center")

        plt.tight_layout()
        plt.savefig("comparacion_canales_visuales.png", dpi=150)
        plt.show()

        # Salida esperada:
        # Se genera un archivo "comparacion_canales_visuales.png" con dos subgráficos.
        # En el gráfico circular es difícil distinguir cuál marca tiene mayor
        # participación (23% vs 21% vs 19%), mientras que en el de barras la
        # diferencia es inmediatamente perceptible.
        ```

    === "Ejemplo 2 — Data-ink ratio"

        Este ejemplo muestra el mismo gráfico de líneas con y sin *chartjunk*, aplicando el
        principio de data-ink ratio.

        ```python
        """
        Ejemplo 2: Aplicación del principio de data-ink ratio (Tufte).
        Requiere: matplotlib, seaborn, numpy
        """
        import matplotlib.pyplot as plt
        import numpy as np
        import seaborn as sns

        # Datos sintéticos: ventas mensuales simuladas
        np.random.seed(42)
        meses = np.arange(1, 13)
        ventas = 100 + np.cumsum(np.random.normal(5, 8, size=12))

        fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

        # --- Versión "chartjunk": exceso de elementos decorativos ---
        ax = axes[0]
        ax.plot(meses, ventas, color="red", linewidth=3, marker="o", markersize=10)
        ax.set_facecolor("#f0e6d2")  # fondo con color innecesario
        ax.grid(True, which="both", color="gray", linewidth=1.5)  # cuadrícula pesada
        ax.set_title("Versión con chartjunk", fontsize=13, fontweight="bold")
        for spine in ax.spines.values():
            spine.set_linewidth(3)  # bordes gruesos innecesarios

        # --- Versión con alto data-ink ratio ---
        sns.set_style("white")
        ax2 = axes[1]
        ax2.plot(meses, ventas, color="#333333", linewidth=2)
        ax2.set_title("Versión con alto data-ink ratio", fontsize=13)
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.set_xlabel("Mes")
        ax2.set_ylabel("Ventas (millones COP)")

        plt.tight_layout()
        plt.savefig("data_ink_ratio.png", dpi=150)
        plt.show()

        # Salida esperada:
        # El panel izquierdo muestra un gráfico recargado (chartjunk): fondo de color,
        # marcadores grandes, cuadrícula pesada y bordes gruesos. El panel derecho
        # muestra la misma información con un diseño minimalista que maximiza el
        # data-ink ratio, facilitando la lectura de la tendencia de ventas.
        ```

!!! example "Ejercicio propuesto"
    1. Descarga o crea un dataset sintético con al menos 6 categorías y un valor
       numérico asociado (por ejemplo, ventas por región).
    2. Construye dos versiones del mismo gráfico: una que use el canal de *ángulo*
       (circular) y otra que use el canal de *posición/longitud* (barras).
    3. Redacta un párrafo (5-8 líneas) argumentando, con base en la jerarquía de
       Cleveland & McGill, cuál de las dos representaciones permite una lectura más
       precisa de los datos y por qué.
    4. Identifica al menos tres elementos de *chartjunk* en un gráfico que hayas
       visto recientemente (una noticia, un reporte corporativo) y propone cómo
       rediseñarlo aplicando el principio de data-ink ratio.

## Referencias

- Tufte, E. R. (2001). *The Visual Display of Quantitative Information* (2nd ed.).
  Graphics Press.
- Cleveland, W. S., & McGill, R. (1984). Graphical Perception: Theory,
  Experimentation, and Application to the Development of Graphical Methods.
  *Journal of the American Statistical Association*, 79(387), 531-554.
- Ware, C. (2012). *Information Visualization: Perception for Design* (3rd ed.).
  Morgan Kaufmann.
- Bertin, J. (1967). *Sémiologie Graphique: Les diagrammes, les réseaux, les
  cartes*. Mouton/Gauthier-Villars.
- Few, S. (2009). *Now You See It: Simple Visualization Techniques for
  Quantitative Analysis*. Analytics Press.
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.
