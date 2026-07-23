"""
Ejemplo 1 (Unidad 3 - Interpolación espacial)
Interpolación IDW (Inverse Distance Weighting) con scipy/numpy.
Requiere: numpy, scipy, matplotlib

Ejecución:
    python 05_idw_interpolacion.py
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist

np.random.seed(5)
n_estaciones = 12
x_estaciones = np.random.uniform(0, 100, n_estaciones)
y_estaciones = np.random.uniform(0, 100, n_estaciones)
temperatura = 30 - 0.08 * y_estaciones + np.random.normal(0, 1.2, n_estaciones)

puntos_muestra = np.column_stack([x_estaciones, y_estaciones])


def interpolacion_idw(puntos_muestra, valores, puntos_estimar, potencia=2):
    """Interpola valores en `puntos_estimar` usando IDW."""
    distancias = cdist(puntos_estimar, puntos_muestra)
    distancias = np.where(distancias == 0, 1e-10, distancias)
    pesos = 1.0 / (distancias ** potencia)
    return (pesos @ valores) / pesos.sum(axis=1)


grid_x, grid_y = np.meshgrid(np.linspace(0, 100, 200), np.linspace(0, 100, 200))
puntos_grid = np.column_stack([grid_x.ravel(), grid_y.ravel()])

temperatura_estimada = interpolacion_idw(
    puntos_muestra, temperatura, puntos_grid, potencia=2
).reshape(grid_x.shape)

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
