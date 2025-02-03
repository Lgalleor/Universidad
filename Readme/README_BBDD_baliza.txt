Explicación del Código

1.Solicitar Ubicación:
	Se solicita la ubicación de la baliza antes de almacenar los datos.

2.Obtención de Datos:
	Se recuperan datos clave de los sensores usando la función fetch_data basada 	en la conexión con la baliza.

3.Manejo de Fechas:
	Se obtiene la fecha y hora actual para usarla como referencia temporal en la 		base de datos.

4.Inserción de Datos:
	Los datos extraídos se almacenan en la tabla baliza_missions con las columnas 	correspondientes.

5.Confirmación de Inserción:
	Se realiza un commit() para guardar los cambios en la base de datos

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Código para Insertar Datos en la Base de Datos

Este código simula la estructura de la base de datos y permite registrar información de la baliza, como su ubicación, alarmas y valores de los sensores.

Proceso del código:

Solicita al usuario el nombre de la misión y la ubicación de la baliza.
Simula la recepción de datos de la baliza (alarma, valores de sensores).
Obtiene la fecha y hora actual.
Inserta los datos en la tabla baliza_missions en la base de datos.
Confirma la inserción con commit().
Resultado:
Los datos de la baliza son almacenados en la base de datos para su posterior consulta.