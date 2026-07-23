"""
Ejemplo 2 (Unidad 3 - Interpolación espacial)
Kriging ordinario básico con PyKrige.
Requiere: pykrige, numpy, matplotlib

Ejecución:
    python 06_kriging_interpolacion.py

Nota: si PyKrige no está disponible en el entorno, instalar con:
    pip install pykrige
"""
import matplotlib.pyplot as plt
import numpy as np
from pykrige.ok import OrdinaryKriging

np.random.seed(5)
n_estaciones = 12
x_estaciones = np.random.uniform(0, 100, n_estaciones)
y_estaciones = np.random.uniform(0, 100, n_estaciones)
temperatura = 30 - 0.08 * y_estaciones + np.random.normal(0, 1.2, n_estaciones)

modelo_kriging = OrdinaryKriging(
    x_estaciones, y_estaciones, temperatura,
    variogram_model="spherical",
    verbose=False,
    enable_plotting=False,
)

grid_x = np.linspace(0, 100, 100)
grid_y = np.linspace(0, 100, 100)
temperatura_estimada, varianza_estimada = modelo_kriging.execute(
    "grid", grid_x, grid_y
)

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
