import sqlite3
import time
import datetime
import random

# Conectar a la base de datos SQLite
conn = sqlite3.connect('dron_data.db')
cur = conn.cursor()

# Crear la tabla si no existe
cur.execute("""
    CREATE TABLE IF NOT EXISTS recorrido_dron (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        opt_m_x REAL,
        opt_m_y REAL,
        opt_qua REAL,
        yaw REAL,
        altitude REAL
    )
""")
conn.commit()

# Simulación de obtención de datos del dron
def obtener_estado_dron():
    """
    Simula la obtención de los valores del dron.
    En un entorno real, estas variables deben provenir del sistema de telemetría.
    """
    return {
        "opt_m_x": round(random.uniform(0, 10), 2),  # Coordenada X simulada
        "opt_m_y": round(random.uniform(0, 10), 2),  # Coordenada Y simulada
        "opt_qua": round(random.uniform(0.5, 1.0), 2),  # Calidad óptica simulada
        "yaw": round(random.uniform(0, 360), 2),  # Ángulo de orientación
        "altitude": round(random.uniform(50, 200), 2)  # Altitud simulada
    }

def guardar_recorrido():
    print("📡 Iniciando la captura de la ruta del dron...")

    i = 35  # Número de registros a capturar
    while i > 0:
        # Obtener datos del dron
        datos = obtener_estado_dron()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insertar los datos en la base de datos
        cur.execute("""
            INSERT INTO recorrido_dron (date, opt_m_x, opt_m_y, opt_qua, yaw, altitude)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, datos["opt_m_x"], datos["opt_m_y"], datos["opt_qua"], datos["yaw"], datos["altitude"]))

        conn.commit()
        print(f"Registro {36 - i}: {timestamp}, X: {datos['opt_m_x']}, Y: {datos['opt_m_y']}, Calidad: {datos['opt_qua']}, Yaw: {datos['yaw']}, Altitud: {datos['altitude']}")

        time.sleep(1)  # Simular adquisición de datos cada 1 segundo
        i -= 1

    print("Ruta del dron almacenada en la base de datos `dron_data.db`.")
    conn.close()

if __name__ == "__main__":
    guardar_recorrido()
