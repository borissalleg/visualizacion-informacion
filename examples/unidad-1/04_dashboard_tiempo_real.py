"""
Ejemplo (Unidad 1 - Visualización dinámica de datos)
Dashboard con actualización periódica usando Streamlit.
Requiere: streamlit, pandas, numpy

Ejecución:
    streamlit run 04_dashboard_tiempo_real.py

El script simula la llegada de datos de un sensor IoT (temperatura y humedad)
y actualiza el dashboard cada segundo, manteniendo una ventana deslizante de
las últimas 50 lecturas.
"""
import time
from collections import deque

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Sensor IoT en tiempo real", layout="wide")
st.title("📡 Dashboard de sensor IoT — actualización en tiempo real")

VENTANA = 50  # número máximo de lecturas a mostrar (sliding window)
INTERVALO_SEGUNDOS = 1

# --- Estado de la sesión: buffers para la ventana deslizante ---
if "tiempos" not in st.session_state:
    st.session_state.tiempos = deque(maxlen=VENTANA)
    st.session_state.temperaturas = deque(maxlen=VENTANA)
    st.session_state.humedades = deque(maxlen=VENTANA)
    st.session_state.tick = 0


def simular_lectura_sensor(tick: int) -> tuple[float, float]:
    """Genera una lectura sintética de temperatura (°C) y humedad (%)."""
    temperatura = 22 + 3 * np.sin(tick / 10) + np.random.normal(0, 0.4)
    humedad = 55 + 10 * np.cos(tick / 15) + np.random.normal(0, 1.2)
    return round(temperatura, 2), round(humedad, 2)


# --- Placeholder que se redibuja en cada iteración ---
placeholder = st.empty()

# NOTA: en un entorno real, este bucle se sustituiría por una suscripción a un
# tópico de Kafka/MQTT o por polling a una API. Aquí se simula con un bucle
# controlado que se detiene tras 200 iteraciones para no bloquear el proceso
# indefinidamente en un entorno de demostración.
for _ in range(200):
    st.session_state.tick += 1
    temp, hum = simular_lectura_sensor(st.session_state.tick)
    st.session_state.tiempos.append(st.session_state.tick)
    st.session_state.temperaturas.append(temp)
    st.session_state.humedades.append(hum)

    df = pd.DataFrame({
        "tick": list(st.session_state.tiempos),
        "temperatura_C": list(st.session_state.temperaturas),
        "humedad_%": list(st.session_state.humedades),
    })

    with placeholder.container():
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperatura actual (°C)", f"{temp:.1f}",
                    f"{temp - df['temperatura_C'].iloc[-2]:.1f}" if len(df) > 1 else None)
        col2.metric("Humedad actual (%)", f"{hum:.1f}")
        col3.metric("Lecturas en ventana", len(df))

        st.line_chart(df.set_index("tick")[["temperatura_C"]])
        st.line_chart(df.set_index("tick")[["humedad_%"]])

    time.sleep(INTERVALO_SEGUNDOS)
