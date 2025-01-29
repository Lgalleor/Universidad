Explicación del Código

1.Lista de sensores y variables clave:
	Se define un diccionario SENSOR_VARIABLES con los sensores más relevantes y 	las variables que miden.

2.Extracción de datos: 
	Se utiliza la función fetch_data de deep_insight_utils para recuperar los 	datos de la baliza.

3.Combinación de datos: 
	Los datos de todos los sensores se combinan en un único DataFrame.

4.Guardado en CSV: 
	Los datos se guardan en baliza_datos_claves.csv para su uso en visualización o 	análisis.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Código para Extracción de Datos de la Baliza

Este código tiene como objetivo extraer los datos más importantes de la baliza utilizando el módulo deep_insight_utils. Se recopilan parámetros clave de los sensores de la baliza, como:

Sensores clave:
BME680: Temperatura, Humedad, Presión, Calidad del aire (IAQ).
SGP30: eCO2, TVOC.
LIS3DH: Aceleración en 3 ejes (X, Y, Z).
Proceso del código:

Define las variables clave de cada sensor.
Usa la función fetch_data() para obtener los datos de la baliza desde una base de datos.
Combina los datos en un DataFrame de Pandas.
Guarda los datos en un archivo CSV (baliza_datos_claves.csv) para su posterior análisis.
Resultado:
Datos listos para ser utilizados en visualización o integración con otras aplicaciones.

