import sqlite3
import pandas as pd
from deep_insight_utils import fetch_data
import datetime

# Definimos las variables clave que queremos extraer de la baliza
SENSOR_VARIABLES = {
    "BME680": ["temperature", "humidity", "pressure", "iaq"],  # Sensores ambientales
    "SGP30": ["eco2", "tvoc"]  # Contaminantes
}

# Información de la baliza
id_device = "DBEM001"
id_sensor = "sWEA"
database = "emergency"

# Obtener la fecha y hora actual para registrar el dato
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Conectar a la base de datos
conn = sqlite3.connect('dron_data.db')
cur = conn.cursor()

# Crear la tabla si no existe, solo con los datos de la baliza
cur.execute("""
    CREATE TABLE IF NOT EXISTS baliza_missions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        temperature REAL,
        humidity REAL,
        pressure REAL,
        iaq REAL,
        eco2 REAL,
        tvoc REAL
    )
""")

# Extraer datos de la baliza
data_dict = {
    "temperature": None, "humidity": None, "pressure": None, "iaq": None,
    "eco2": None, "tvoc": None
}

for sensor, variables in SENSOR_VARIABLES.items():
    for variable in variables:
        data = fetch_data(
            id_device=id_device,
            id_sensor=id_sensor,
            id_variable=variable,
            init_str=current_time,
            end_str=current_time,
            database=database
        )

        if data is not None and not data.empty:
            data_dict[variable] = data.iloc[-1]["value"]  # Tomar el último valor recibido

# Insertar los datos en la base de datos sin ubicación
cur.execute("""
    INSERT INTO baliza_missions (date, temperature, humidity, pressure, iaq, eco2, tvoc)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", (current_time, data_dict["temperature"], data_dict["humidity"], data_dict["pressure"],
      data_dict["iaq"], data_dict["eco2"], data_dict["tvoc"]))

conn.commit()
conn.close()
print("✅ Datos de la baliza insertados correctamente en la base de datos.")
