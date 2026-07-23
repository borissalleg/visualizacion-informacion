"""
Ejemplo (Unidad 1 - Tipos de visualización)
Datos crudos vs. datos procesados.
Requiere: pandas, numpy, matplotlib

Ejecución:
    python 03_crudo_vs_procesado.py
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

# --- 2. Datos procesados: KPIs agregados por región ---
kpis = df.groupby("region")["monto_venta"].agg(
    total="sum", promedio="mean", mediana="median", desviacion="std", n="count"
).round(2).sort_values("total", ascending=False)

print("\n=== KPIs agregados por región ===")
print(kpis)

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
