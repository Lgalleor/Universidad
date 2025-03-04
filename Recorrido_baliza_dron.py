import plotly.graph_objects as go
import sqlite3
import pandas as pd

# Función para asignar colores según el valor de IAQ (calidad del aire)
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

# Obtener los datos del recorrido del dron
cur.execute("SELECT date, latitude, longitude, altitude FROM recorrido_dron")
recorrido_data = cur.fetchall()

# Obtener los datos de la baliza (calidad del aire en cada punto del recorrido)
cur.execute("SELECT date, latitude, longitude, altitude, sensor1 FROM baliza_missions")
baliza_data = cur.fetchall()

conn.close()

# Verificar si hay datos disponibles en ambas tablas
if not recorrido_data or not baliza_data:
    print("⚠️ No hay datos suficientes en la base de datos.")
    exit()

# Convertir los datos del recorrido del dron en un DataFrame
recorrido_df = pd.DataFrame(recorrido_data, columns=["date", "latitude", "longitude", "altitude"])

# Convertir los datos de la baliza en un DataFrame
baliza_df = pd.DataFrame(baliza_data, columns=["date", "latitude", "longitude", "altitude", "iaq"])

# Unir los datos del recorrido con los datos de la baliza usando la fecha, latitud y longitud como clave
merged_df = pd.merge(recorrido_df, baliza_df, on=["date", "latitude", "longitude", "altitude"], how="inner")

# Extraer listas de datos para la visualización
latitudes = merged_df["latitude"].tolist()
longitudes = merged_df["longitude"].tolist()
altitudes = merged_df["altitude"].tolist()
iaq_values = merged_df["iaq"].tolist()
colors = [get_color(iaq) for iaq in iaq_values]

# Crear el gráfico 3D interactivo
fig = go.Figure()

# Añadir puntos del recorrido del dron con los datos de calidad del aire
for i in range(len(latitudes)):
    fig.add_trace(go.Scatter3d(
        x=[longitudes[i]],
        y=[latitudes[i]],
        z=[altitudes[i]],
        mode='markers',
        marker=dict(size=10, color=colors[i]),
        text=f"📅 Fecha: {merged_df['date'].iloc[i]}<br>💨 IAQ: {iaq_values[i]}",
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
