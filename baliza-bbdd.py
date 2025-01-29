#guardar los datos en la baliza
import sqlite3
import datetime
import pandas as pd
from deep_insight_utils import fetch_data

# Definir las variables clave a extraer de la baliza
SENSOR_VARIABLES = {
    "BME680": ["00-temp", "01-hum", "02-pres", "03-siaq"],
    "SGP30": ["00-eco2", "01-tvoc"],
    "LIS3DH": ["00-accx", "01-accy", "02-accz"]
}

# Solicitar la ubicación de la baliza
print("Introduce la ubicación de la baliza:")
location = input()

# Conectar a la base de datos
conn = sqlite3.connect('dron_data.db')
cur = conn.cursor()

# Crear la tabla si no existe
cur.execute("""
    CREATE TABLE IF NOT EXISTS baliza_missions (
        date TEXT,
        data_type TEXT,
        location TEXT,
        alarma TEXT,
        sensor1 REAL,
        sensor2 REAL,
        sensor3 REAL,
        sensor4 REAL,
        sensor5 REAL
    )
""")

# Obtener la fecha y hora actual
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Información de la baliza
id_device = "DBEM001"
id_sensor = "sWEA"
database = "emergency"

# Extraer datos en tiempo real de la baliza
all_sensor_data = []

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
            data["sensor"] = sensor
            data["variable"] = variable
            all_sensor_data.append(data)

# Procesar los datos obtenidos y seleccionar las 5 variables más recientes
if all_sensor_data:
    final_df = pd.concat(all_sensor_data, ignore_index=True)

    # Seleccionar solo las últimas 5 mediciones
    latest_data = final_df[['variable', 'value']].iloc[-5:].values

    # Extraer los valores para la inserción en la base de datos
    sensor1, sensor2, sensor3, sensor4, sensor5 = latest_data[:, 1]

    # Determinar el estado de la alarma según los valores obtenidos
    alarma = "normal"
    if max(sensor1, sensor2, sensor3, sensor4, sensor5) > 300:  # Umbral de alerta (puede ajustarse)
        alarma = "alerta"

    # Insertar datos en la base de datos
    cur.execute("""
        INSERT INTO baliza_missions (date, data_type, location, alarma, sensor1, sensor2, sensor3, sensor4, sensor5)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (current_time, 'BALIZA', location, alarma, sensor1, sensor2, sensor3, sensor4, sensor5))

    conn.commit()
    print("Datos insertados correctamente en la base de datos.")

else:
    print("No se encontraron datos para los sensores especificados.")

conn.close()