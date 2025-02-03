Código para Visualización del Recorrido del Dron

Este código se encarga de visualizar el recorrido del dron en un gráfico 3D utilizando plotly. El recorrido se presenta en función de coordenadas espaciales simuladas.

Proceso del código:
Genera datos de coordenadas del dron (latitud, longitud, altitud).
Simula valores de calidad del aire asociados a cada punto del recorrido.
Asigna colores a los puntos en función de los niveles de calidad del aire.
Visualiza el recorrido en un mapa 3D con puntos interactivos que muestran información detallada al pasar el cursor.
Guarda el gráfico en un archivo HTML (recorrido_dron.html).

Resultado:
Un gráfico interactivo en 3D que muestra el recorrido del dron con información detallada de calidad del aire.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Explicación de las Mejoras

1. Obtención de Datos en Tiempo Real:
	Se ha agregado la función obtener_datos_dron() que simula una API de telemetría.
	Se almacenan nuevas lecturas en la base de datos cada 2 segundos en la función 	guardar_datos().

2.Filtrado de Datos por Fecha:
	La función obtener_datos_desde_bd(start_date, end_date) permite seleccionar datos en un 	rango de fechas.
	El usuario puede ingresar fechas de inicio y fin para analizar datos específicos.

3.Exportación de Datos:
	Se pueden exportar datos a CSV con la función exportar_a_csv().
	Se pueden exportar a JSON con la función exportar_a_json().

4.Visualización Mejorada:
	La función visualizar_mapa() genera gráficos con la opción de filtrar datos por fecha.
	Los puntos muestran información detallada al pasar el cursor.

5.Menú Interactivo:
	Un menú de consola guía al usuario a través de las diferentes opciones (recolectar 	datos, visualización, exportación, salida).
