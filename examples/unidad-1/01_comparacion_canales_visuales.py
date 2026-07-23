"""
Ejemplo 1 (Unidad 1 - Conceptos teóricos y fundamentos)
Comparación de canales visuales — posición vs. ángulo.
Requiere: matplotlib

Ejecución:
    python 01_comparacion_canales_visuales.py
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
