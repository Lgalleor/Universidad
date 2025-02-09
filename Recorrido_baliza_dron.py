#recorrido dron

import plotly.graph_objects as go
import sqlite3
import pandas as pd

# Función para asignar colores según el valor de IAQ
def get_color(iaq):
    if iaq <= 50:
        return "green"
    elif 51 <= iaq <= 100:
        return "yellow"
    elif 101 <= iaq <= 150:
        return "orange"
    elif 151 <= iaq <= 200:
        return "red"
    elif 201 <= iaq <= 250:
        return "purple"
    elif 251 <= iaq <= 350:
        return "brown"
    else:
        return "black"

# Conectar a la base de datos y recuperar datos
conn = sqlite3.connect('dron_data.db')
cur = conn.cursor()
cur.execute("SELECT latitude, longitude, altitude, sensor1 FROM baliza_missions")
data = cur.fetchall()
conn.close()

# Extraer coordenadas y datos del sensor
latitudes, longitudes, altitudes, iaq_values = zip(*data)
colors = [get_color(iaq) for iaq in iaq_values]

# Crear el gráfico 3D interactivo
fig = go.Figure()

# Añadir puntos del recorrido del dron
for i in range(len(latitudes)):
    fig.add_trace(go.Scatter3d(
        x=[longitudes[i]],
        y=[latitudes[i]],
        z=[altitudes[i]],
        mode='markers',
        marker=dict(size=10, color=colors[i]),
        text=f"IAQ: {iaq_values[i]}",
        hoverinfo="text"
    ))

# Configuración del gráfico
fig.update_layout(
    title="Recorrido del Dron con Calidad del Aire",
    scene=dict(
        xaxis_title="Longitud",
        yaxis_title="Latitud",
        zaxis_title="Altitud",
        bgcolor="black"
    ),
    paper_bgcolor="black",
    font=dict(color="white")
)

# Mostrar gráfico
fig.show()
