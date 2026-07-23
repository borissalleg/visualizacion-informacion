"""
Ejemplo 2 (Unidad 3 - Mapas de densidad)
Estimación de densidad por kernel (KDE) con Seaborn.
Requiere: seaborn, matplotlib, numpy, pandas

Ejecución:
    python 04_kde_densidad_seaborn.py
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

np.random.seed(21)
focos = [(6.2442, -75.5812, 300), (6.2087, -75.5679, 220), (6.2650, -75.5900, 150)]
puntos = []
for lat_c, lon_c, n in focos:
    lats = np.random.normal(lat_c, 0.006, n)
    lons = np.random.normal(lon_c, 0.006, n)
    puntos.extend(zip(lats, lons))

df = pd.DataFrame(puntos, columns=["lat", "lon"])

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

for ax, bw in zip(axes, [0.1, 0.5, 2.0]):
    sns.kdeplot(
        data=df, x="lon", y="lat", fill=True, cmap="rocket_r",
        bw_adjust=bw, thresh=0.05, ax=ax,
    )
    sns.scatterplot(data=df, x="lon", y="lat", s=5, color="black", alpha=0.3, ax=ax)
    ax.set_title(f"bw_adjust = {bw}")

plt.suptitle("Efecto del ancho de banda (bandwidth) en la estimación KDE")
plt.tight_layout()
plt.savefig("kde_densidad_seaborn.png", dpi=150)
plt.show()
