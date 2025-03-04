import sqlite3
import datetime
import time
import random

# Función para obtener datos simulados del recorrido del dron
def obtener_datos_dron():
    return {
        "latitude": 40.416 + random.uniform(-0.01, 0.01),
        "longitude": -3.703 + random.uniform(-0.01, 0.01),
        "altitude": random.uniform(100, 300)
    }

# Conectar a la base de datos SQLite 
conn = sqlite3.connect('dron_data.db')
cur = conn.cursor()

# Crear la tabla si no existe
cur.execute("""
    CREATE TABLE IF NOT EXISTS recorrido_dron (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        latitude REAL,
        longitude REAL,
        altitude REAL
    )
""")

# Guardar datos en la base de datos
print("Iniciando la grabación del recorrido del dron...")

for _ in range(20):  # Simular 20 puntos del recorrido
    datos = obtener_datos_dron()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute("""
        INSERT INTO recorrido_dron (date, latitude, longitude, altitude)
        VALUES (?, ?, ?, ?)
    """, (timestamp, datos["latitude"], datos["longitude"], datos["altitude"]))

    conn.commit()
    print(f"Punto registrado: {timestamp}, Lat: {datos['latitude']}, Lon: {datos['longitude']}, Alt: {datos['altitude']}m")

    time.sleep(2)  # Simular tiempo entre capturas de datos

conn.close()
print("Recorrido del dron guardado en la base de datos `dron_data.db`.")
