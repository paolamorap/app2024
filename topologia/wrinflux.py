from influxdb import InfluxDBClient
import time
# Conexión al servidor InfluxDB
client = InfluxDBClient(host='localhost', port=8086, username='admin', password='admin', database='influx')
data = []
def wr_influx(datos):
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
    
