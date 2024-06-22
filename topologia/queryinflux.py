from influxdb import InfluxDBClient

# Configurar la conexión a la base de datos InfluxDB
client = InfluxDBClient(host='127.0.0.1', port=8086, database='Monitoreo')

# Escribir una consulta InfluxQL
query = 'SELECT * FROM "interrumpciones"'

# Ejecutar la consulta
result = client.query(query)

# Recorrer los resultados
for point in result.get_points():
    print(point)

# Cerrar la conexión
client.close()