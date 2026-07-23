"""
Ejemplo 2 (Unidad 1 - Conceptos teóricos y fundamentos)
Aplicación del principio de data-ink ratio (Tufte).
Requiere: matplotlib, seaborn, numpy

Ejecución:
    python 02_data_ink_ratio.py
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
