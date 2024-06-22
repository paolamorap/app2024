from influxdb import InfluxDBClient

# Configurar la conexión a la base de datos InfluxDB
client = InfluxDBClient(host='127.0.0.1', port=8086, database='influx')



# Lista de direcciones IP de los agentes que deseas consultar
agentes = ['10.0.1.1', '10.0.1.2','10.0.1.3','10.0.1.4','10.0.1.5','10.0.1.6']

def con_uptime(agentes):
    infuptime = {}
    for agente in agentes:
        query = f'SELECT last("uptime") FROM "snmp" WHERE ("agent_host" = \'{agente}\') AND time >= now() - 10s AND time <= now() fill(null)'
        
        # Ejecutar la consulta para el agente actual
        result = client.query(query)
        
        # Imprimir los resultados para el agente actual
        for point in result.get_points():
            infuptime[agente] = float(point["last"])

    # Cerrar la conexión
    client.close()
    return infuptime

print(con_uptime(agentes))