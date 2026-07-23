## Interpolación espacial

> ### Objetivos de aprendizaje
> Al finalizar este subtema, el estudiante será capaz de:
>
> - Explicar el concepto de interpolación espacial y su utilidad para estimar
>   valores en ubicaciones no muestreadas.
> - Implementar el método de Ponderación por Distancia Inversa (IDW, *Inverse
>   Distance Weighting*) con `scipy`.
> - Comprender los fundamentos del Kriging como método geoestadístico e
>   implementar un ejemplo básico con `PyKrige`.

=== "1. ¿Qué es la interpolación espacial?"

    La **interpolación espacial** es el conjunto de técnicas que permiten **estimar
    el valor de una variable continua en ubicaciones donde no se tomó una medición
    directa**, a partir de un conjunto de puntos de muestra con valores conocidos. Es
    fundamental en disciplinas como la meteorología (estimar temperatura o
    precipitación entre estaciones), la agricultura de precisión (estimar humedad del
    suelo entre sensores) y la calidad ambiental (estimar concentración de
    contaminantes entre estaciones de monitoreo).

    El principio subyacente es la **primera ley de la geografía de Tobler**:

    > *"Everything is related to everything else, but near things are more related
    > than distant things"* (Todo está relacionado con todo lo demás, pero las cosas
    > cercanas están más relacionadas que las distantes).

    Esto justifica que, para estimar un valor en un punto sin medición, se le dé más
    peso a las observaciones cercanas que a las lejanas.

=== "2. IDW vs. Kriging"

    === "2.1 Ponderación por Distancia Inversa (IDW)"

        El método **IDW (Inverse Distance Weighting)** estima el valor en un punto no
        muestreado como un **promedio ponderado** de los valores conocidos, donde el peso
        de cada observación es inversamente proporcional a su distancia al punto de
        interés, elevada a una potencia $p$:

        $$
        \hat{z}(x_0) = \frac{\sum_{i=1}^{n} w_i \, z(x_i)}{\sum_{i=1}^{n} w_i}, \quad
        \text{donde } w_i = \frac{1}{d(x_0, x_i)^p}
        $$

        - $z(x_i)$: valor conocido en el punto de muestra $i$.
        - $d(x_0, x_i)$: distancia entre el punto a estimar $x_0$ y el punto de muestra
          $x_i$.
        - $p$: parámetro de potencia (usualmente 2), que controla cuán rápido decae la
          influencia de un punto con la distancia. A mayor $p$, más "local" es la
          influencia de los puntos cercanos.

        **Ventajas de IDW**: simple de implementar e interpretar, determinístico (mismo
        resultado siempre), computacionalmente económico.

        **Limitaciones**: no proporciona una medida de incertidumbre de la estimación, y
        puede generar el conocido efecto de "ojo de buey" (*bullseye effect*) alrededor de
        los puntos de muestra —círculos concéntricos visibles en el mapa interpolado.

    === "2.2 Kriging (geoestadístico)"

        El **Kriging** (nombrado en honor al ingeniero sudafricano Danie G. Krige) es un
        método de interpolación **geoestadístico** que, a diferencia de IDW, modela
        explícitamente la **estructura de autocorrelación espacial** de los datos mediante
        un **variograma** (o semivariograma), y produce no solo una estimación puntual
        sino también una **varianza de la estimación** (una medida de incertidumbre).

        El variograma cuantifica cómo la similitud entre pares de puntos decrece con la
        distancia, y el Kriging usa este modelo para calcular los pesos óptimos (en el
        sentido de mínima varianza y sin sesgo) que se aplican a cada observación conocida.

        !!! note "El variograma"
            El variograma empírico se calcula agrupando pares de puntos por distancia y
            calculando la semivarianza promedio de sus diferencias. Luego se ajusta un
            modelo teórico (esférico, exponencial, gaussiano) a esos puntos empíricos.
            Este modelo ajustado es el que Kriging usa internamente para ponderar las
            observaciones.

        | Característica | IDW | Kriging |
        |---|---|---|
        | Base teórica | Heurística (distancia inversa) | Geoestadística (variograma, autocorrelación espacial) |
        | Provee incertidumbre | No | Sí (varianza de Kriging) |
        | Complejidad de implementación | Baja | Media-alta (requiere ajustar el variograma) |
        | Sensible a la anisotropía | Limitado | Sí, puede modelarse explícitamente |
        | Caso de uso típico | Estimaciones rápidas, exploratorias | Estudios ambientales/geológicos rigurosos con necesidad de cuantificar incertidumbre |

        !!! warning "Errores comunes"
            Aplicar Kriging (o IDW) para extrapolar **fuera** del área convexa cubierta
            por los puntos de muestra puede producir estimaciones poco confiables: ambos
            métodos son técnicas de **interpolación**, no de extrapolación, y su fiabilidad
            decae rápidamente fuera del rango espacial muestreado. Además, un número muy
            bajo de estaciones de muestreo (menos de ~10-15) hace poco confiable el ajuste
            de un variograma robusto para Kriging.

=== "3. Ejemplos de código"

    === "IDW con scipy"

        Se simulan 12 estaciones meteorológicas con mediciones de temperatura, y se
        estima la temperatura en una malla continua del territorio.

        ```python
        """
        Ejemplo 1: Interpolación IDW (Inverse Distance Weighting) con scipy/numpy.
        Requiere: numpy, scipy, matplotlib

        Ejecución:
            python idw_interpolacion.py
        """
        import matplotlib.pyplot as plt
        import numpy as np
        from scipy.spatial.distance import cdist

        # --- 1. Datos sintéticos: 12 "estaciones meteorológicas" con temperatura (°C) ---
        np.random.seed(5)
        n_estaciones = 12
        x_estaciones = np.random.uniform(0, 100, n_estaciones)
        y_estaciones = np.random.uniform(0, 100, n_estaciones)
        # Temperatura simulada con un gradiente norte-sur más ruido aleatorio
        temperatura = 30 - 0.08 * y_estaciones + np.random.normal(0, 1.2, n_estaciones)

        puntos_muestra = np.column_stack([x_estaciones, y_estaciones])


        def interpolacion_idw(puntos_muestra, valores, puntos_estimar, potencia=2):
            """Interpola valores en `puntos_estimar` usando IDW."""
            distancias = cdist(puntos_estimar, puntos_muestra)
            # Evitar división por cero cuando un punto a estimar coincide con una muestra
            distancias = np.where(distancias == 0, 1e-10, distancias)
            pesos = 1.0 / (distancias ** potencia)
            return (pesos @ valores) / pesos.sum(axis=1)


        # --- 2. Malla continua sobre la cual estimar la temperatura ---
        grid_x, grid_y = np.meshgrid(np.linspace(0, 100, 200), np.linspace(0, 100, 200))
        puntos_grid = np.column_stack([grid_x.ravel(), grid_y.ravel()])

        temperatura_estimada = interpolacion_idw(
            puntos_muestra, temperatura, puntos_grid, potencia=2
        ).reshape(grid_x.shape)

        # --- 3. Visualización ---
        fig, ax = plt.subplots(figsize=(7, 6))
        contorno = ax.contourf(grid_x, grid_y, temperatura_estimada, levels=20, cmap="coolwarm")
        ax.scatter(x_estaciones, y_estaciones, c=temperatura, cmap="coolwarm",
                   edgecolor="black", s=80, label="Estaciones meteorológicas")
        plt.colorbar(contorno, label="Temperatura estimada (°C)")
        ax.set_title("Interpolación IDW de temperatura a partir de 12 estaciones")
        ax.set_xlabel("Coordenada X (km)")
        ax.set_ylabel("Coordenada Y (km)")
        ax.legend(loc="upper right")
        plt.tight_layout()
        plt.savefig("idw_interpolacion.png", dpi=150)
        plt.show()

        # Salida esperada:
        # Un mapa de contorno relleno (superficie continua) que estima la temperatura
        # en todo el territorio a partir de las 12 estaciones puntuales, con un
        # gradiente cálido (rojo) en la zona sur y frío (azul) en la zona norte,
        # consistente con el patrón sintético introducido. Alrededor de cada estación
        # se puede apreciar un leve efecto de "ojo de buey" característico de IDW.
        ```

    === "Kriging con PyKrige"

        ```python
        """
        Ejemplo 2: Kriging ordinario básico con PyKrige.
        Requiere: pykrige, numpy, matplotlib

        Ejecución:
            python kriging_interpolacion.py

        Nota: si PyKrige no está disponible en el entorno, instalar con:
            pip install pykrige
        """
        import matplotlib.pyplot as plt
        import numpy as np
        from pykrige.ok import OrdinaryKriging

        # --- 1. Mismos datos sintéticos de estaciones meteorológicas que en IDW ---
        np.random.seed(5)
        n_estaciones = 12
        x_estaciones = np.random.uniform(0, 100, n_estaciones)
        y_estaciones = np.random.uniform(0, 100, n_estaciones)
        temperatura = 30 - 0.08 * y_estaciones + np.random.normal(0, 1.2, n_estaciones)

        # --- 2. Ajuste del modelo de Kriging Ordinario con variograma esférico ---
        modelo_kriging = OrdinaryKriging(
            x_estaciones, y_estaciones, temperatura,
            variogram_model="spherical",
            verbose=False,
            enable_plotting=False,
        )

        # --- 3. Estimación sobre una malla continua ---
        grid_x = np.linspace(0, 100, 100)
        grid_y = np.linspace(0, 100, 100)
        temperatura_estimada, varianza_estimada = modelo_kriging.execute(
            "grid", grid_x, grid_y
        )

        # --- 4. Visualización: estimación y varianza (incertidumbre) ---
        fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

        im1 = axes[0].contourf(grid_x, grid_y, temperatura_estimada, levels=20, cmap="coolwarm")
        axes[0].scatter(x_estaciones, y_estaciones, c=temperatura, cmap="coolwarm",
                        edgecolor="black", s=80)
        plt.colorbar(im1, ax=axes[0], label="Temperatura estimada (°C)")
        axes[0].set_title("Kriging Ordinario — Estimación")

        im2 = axes[1].contourf(grid_x, grid_y, varianza_estimada, levels=20, cmap="viridis")
        axes[1].scatter(x_estaciones, y_estaciones, c="white", edgecolor="black", s=60)
        plt.colorbar(im2, ax=axes[1], label="Varianza de Kriging")
        axes[1].set_title("Kriging Ordinario — Incertidumbre (varianza)")

        plt.tight_layout()
        plt.savefig("kriging_interpolacion.png", dpi=150)
        plt.show()

        # Salida esperada:
        # Panel izquierdo: superficie de temperatura estimada, similar en tendencia
        # general a la de IDW, pero con transiciones más suaves gracias al modelo de
        # variograma ajustado. Panel derecho: mapa de varianza de Kriging, donde la
        # incertidumbre es baja (colores oscuros) cerca de las estaciones de muestreo
        # y aumenta (colores claros) en zonas alejadas de cualquier estación,
        # evidenciando la principal ventaja de Kriging sobre IDW: cuantificar dónde
        # la estimación es más o menos confiable.
        ```

    !!! tip "Buenas prácticas"
        - Antes de aplicar Kriging, examina siempre el variograma empírico: si no
          muestra una estructura espacial clara (una relación creciente entre
          distancia y semivarianza que luego se estabiliza), el supuesto de
          autocorrelación espacial puede no sostenerse y IDW podría ser preferible.
        - Reporta siempre el mapa de varianza junto con el de estimación al comunicar
          resultados de Kriging: un mapa de estimación sin su incertidumbre asociada
          puede sugerir una falsa precisión.
        - Valida el modelo con **validación cruzada dejando uno fuera**
          (*leave-one-out cross-validation*): remueve temporalmente cada estación,
          estima su valor con las demás y compara contra el valor real medido.

!!! example "Ejercicio propuesto"
    1. Genera un conjunto sintético de 20 "estaciones de calidad del aire" con
       una variable (ej. concentración de PM2.5) que tenga un gradiente
       espacial claro (por ejemplo, mayor cerca de una "zona industrial"
       simulada).
    2. Aplica IDW con al menos dos valores distintos del parámetro de potencia
       ($p = 1$ y $p = 3$) y compara visualmente el efecto sobre la suavidad del
       mapa resultante.
    3. Aplica Kriging Ordinario sobre el mismo conjunto de datos y compara el
       mapa de estimación con el de IDW. Redacta un párrafo (5-8 líneas)
       explicando en qué escenario de la vida real elegirías Kriging sobre IDW,
       considerando el costo computacional adicional y la necesidad (o no) de
       cuantificar incertidumbre.

## Referencias

- Tobler, W. R. (1970). A Computer Movie Simulating Urban Growth in the Detroit
  Region. *Economic Geography*, 46(sup1), 234-240.
- Cressie, N. (1993). *Statistics for Spatial Data* (Revised ed.). Wiley.
- Isaaks, E. H., & Srivastava, R. M. (1989). *An Introduction to Applied
  Geostatistics*. Oxford University Press.
- Documentación oficial de PyKrige: <https://geostat-framework.readthedocs.io/projects/pykrige/>
- Documentación de `scipy.spatial.distance.cdist`:
  <https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html>
