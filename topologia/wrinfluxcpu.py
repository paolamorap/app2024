from influxdb import InfluxDBClient
import time
# Conexión al servidor InfluxDB
client = InfluxDBClient(host='localhost', port=8086, username='admin', password='admin', database='influx')

def wr_influx(datos):
    """
    Permite escribir en una base de Datos de InfluxDB las interrumpciones que ha tenido un equipo
    Esta función estara ligada a una lógica previa que determianra si se escriben los datos
    
    Parameters:
    datos(dict): Diccionario con información de los switches de la Red

    Return:
    Registro de datos acerca del consumo de CPU en los dispositivos
    """
    
    data = []
    direc = list(datos.keys())
    for ip in direc:
        try:    
            d1 = {
                    "measurement": "cpupython",
                    "tags": {
                        "dispositivo": str(ip)
                    },
                    "fields": {
                        "uso5min": float(datos[ip])
                    }
                }
        except TypeError:
            pass
        data.append(d1)
    client.write_points(data)
    time.sleep(1)
    client.close()