#datos_baliza
import pandas as pd
from deep_insight_utils import fetch_data

# Definimos las variables clave que queremos extraer
SENSOR_VARIABLES = {
    "BME680": ["00-temp", "01-hum", "02-pres", "03-siaq"],
    "SGP30": ["00-eco2", "01-tvoc"],
    "LIS3DH": ["00-accx", "01-accy", "02-accz"]
}

# Parámetros de la baliza (ejemplo, reemplazar con valores reales)
id_device = "DBEM001"
id_sensor = "sWEA"
init_str = "2024-01-01 00:00:00"
end_str = "2024-01-02 00:00:00"
database = "emergency"

# Extraer datos de cada sensor
all_sensor_data = []

for sensor, variables in SENSOR_VARIABLES.items():
    for variable in variables:
        data = fetch_data(
            id_device=id_device,
            id_sensor=id_sensor,
            id_variable=variable,
            init_str=init_str,
            end_str=end_str,
            database=database
        )

        if data is not None and not data.empty:
            data["sensor"] = sensor
            data["variable"] = variable
            all_sensor_data.append(data)

# Combinar todos los datos en un solo DataFrame
if all_sensor_data:
    final_df = pd.concat(all_sensor_data, ignore_index=True)

    # Mostrar las primeras filas de los datos recopilados
    print(final_df.head())

    # Guardar los datos en un archivo CSV para su análisis posterior
    final_df.to_csv("baliza_datos_claves.csv", index=False)

    print("Datos guardados en 'baliza_datos_claves.csv'")
else:
    print("No se encontraron datos para los sensores especificados.")
