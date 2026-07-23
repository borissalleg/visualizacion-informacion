"""
Ejemplo (Unidad 2 - Librerías de visualización)
El mismo gráfico (esperanza de vida vs. PIB per cápita) con Matplotlib,
Seaborn y Plotly, para comparar sintaxis y resultado.
Requiere: pandas, numpy, matplotlib, seaborn, plotly

Ejecución:
    python 03_comparativa_librerias.py
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns

# --- Datos sintéticos compartidos ---
np.random.seed(10)
paises = ["Colombia", "Brasil", "México", "Argentina", "Chile", "Perú",
          "Ecuador", "Bolivia", "Uruguay", "Paraguay"]

df = pd.DataFrame({
    "pais": paises,
    "pib_per_capita": np.random.uniform(4000, 25000, size=len(paises)).round(0),
    "esperanza_vida": np.random.uniform(70, 82, size=len(paises)).round(1),
    "poblacion_millones": np.random.uniform(3, 220, size=len(paises)).round(1),
})
print(df)

# --- 1. Matplotlib ---
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(
    df["pib_per_capita"], df["esperanza_vida"],
    s=df["poblacion_millones"] * 3,
    alpha=0.6, c=range(len(df)), cmap="viridis",
)
for _, row in df.iterrows():
    ax.annotate(row["pais"], (row["pib_per_capita"], row["esperanza_vida"]),
                fontsize=8, xytext=(4, 4), textcoords="offset points")
ax.set_xlabel("PIB per cápita (USD)")
ax.set_ylabel("Esperanza de vida (años)")
ax.set_title("Esperanza de vida vs. PIB per cápita (Matplotlib)")
plt.tight_layout()
plt.savefig("comparativa_matplotlib.png", dpi=150)
plt.close(fig)

# --- 2. Seaborn ---
plt.figure(figsize=(8, 5))
sns.scatterplot(
    data=df, x="pib_per_capita", y="esperanza_vida",
    size="poblacion_millones", sizes=(50, 500),
    hue="pais", legend=False, alpha=0.7,
)
plt.title("Esperanza de vida vs. PIB per cápita (Seaborn)")
plt.xlabel("PIB per cápita (USD)")
plt.ylabel("Esperanza de vida (años)")
plt.tight_layout()
plt.savefig("comparativa_seaborn.png", dpi=150)
plt.close()

# --- 3. Plotly ---
fig_plotly = px.scatter(
    df, x="pib_per_capita", y="esperanza_vida",
    size="poblacion_millones", color="pais", text="pais",
    title="Esperanza de vida vs. PIB per cápita (Plotly)",
    labels={"pib_per_capita": "PIB per cápita (USD)",
            "esperanza_vida": "Esperanza de vida (años)"},
    size_max=60,
)
fig_plotly.update_traces(textposition="top center")
fig_plotly.update_layout(template="plotly_white")
fig_plotly.write_html("comparativa_plotly.html", include_plotlyjs="cdn")

print("Archivos generados: comparativa_matplotlib.png, comparativa_seaborn.png,"
      " comparativa_plotly.html")
