from influxdb import InfluxDBClient
import time
# Conexión al servidor InfluxDB
client = InfluxDBClient(host='localhost', port=8086, username='admin', password='admin', database='influx')

def wr_influx(datos):
    """
    Permite escribir en una base de Datos de InfluxDB
    
    Parameters:
    datos(dict): Diccionario con información de los switches de la Red

    Return:
    Registro de datos en la base de datos
    """
    data = []
    direc = list(datos.keys())
    for ip in direc:
        d1 = {
                "measurement": "interrumpciones",
                "tags": {
                    "dispositivo": str(ip)
                },
                "fields": {
                    "interrupciones": float(datos[ip])
                }
            }
        data.append(d1)
    client.write_points(data)
    time.sleep(1)
    client.close()