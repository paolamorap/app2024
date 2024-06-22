import obt_infyam
import teleg
from influxdb import InfluxDBClient
import numpy as np
import time
import os

#Valores de configuración del script
current_dir = os.path.dirname(__file__)
config_file = current_dir+'/configuracion/configuracion_monitoreo.json'
config = obt_infyam.read_config(config_file)
cputime = config.get('cputiempo', 20)  
cpuvalref = config.get('cpuvalref', 10)  

# Configurar la conexión a la base de datos InfluxDB
client = InfluxDBClient(host='127.0.0.1', port=8086, database='influx')

def obt_cpudata(agentes):
    """
    Funcion para obtener los datos de consumo de cpu por dispositvo. 
    Retorna un valor promediado de consumo en los ultimos 30 min

    Parámetros:
    agentes (list): Lista con las direcciones IP de los dispositivos

    Retunrs:
    infcpuconsum (dict) :  Diccionario con el consumo por dispositivo
    
    """
    infcpuconsum = {}
    for agente in agentes:
        datos = []
        query = f'SELECT ("uso5min") FROM "cpupython" WHERE ("dispositivo" = \'{agente}\') AND time >= now() - {cputime}m AND time <= now() fill(null)'
        # Ejecutar la consulta para el agente actual
        result = client.query(query)
        for point in result.get_points():
            datos.append(float(point["uso5min"]))
    
        des_esta = np.std(datos)
        media = np.mean(datos)
        mediana = np.median(datos)
        pico = max(datos)

        infcpuconsum[agente] = [des_esta,media,pico,mediana]

    # Cerrar la conexión
    client.close()
    return infcpuconsum

def warning_cpu(vn,datacpu):
    """
    Función para emitir una alerta a Telegram mediante un análisis de los datos

    Parámetros:
    datacpu(dict) :  Diccionario con los datos de consumo de cpu por dispositivo
    vn(int):         Valor Referencial de Consumo Normal 

    Returns:
    none:             Envia advertencia 
    """

    mvar = ""
    mdes =""
    detalles=""
    
    for disp in datacpu.keys():
        desviacion = datacpu[disp][0]
        media = datacpu[disp][1]
        pico = datacpu[disp][2]
        mediana = datacpu[disp][3]
        f = False
        #Apartado para pruebas - visualización de datos
        cab = "-"*10+"Estadisticas: "+disp+"-"*10
        print(cab)
        print("Desviación estandar: ",desviacion)
        print("Media: ",media)
        print("Mediana: ",mediana)
        print("Valor Max: ",pico)
        print("-"*len(cab))
        #Clasificación de notificaciones   


        if pico >= vn + 5 and mediana <= vn:
            mdes = "Hubo un gran consumo por un momento"
            f = True


        if desviacion >= 0.5:
            mvar = "Variaciones Ligeras de Consumo"
            f = True
        if desviacion >= 1.5:
            mvar = "Variaciones Moderadas de Consumo"
            f = True
        if desviacion >= 3.5:
            mvar = "Variaciones Rápidas de Consumo"
            f = True

        if media >= vn + 1.5:
            mdes = "Consumo de CPU levemente alto"
            f = True
        if media >= vn + 5:
            mdes = "Consumo de CPU alto por un tiempo considerable"
            f = True
        if  media >= vn + 8:
            mdes = "Consumo de CPU muy alto por un largo periodo de tiempo"
            f = True

        #Detalles de Consumo
        detalles = "--------------NOTIFICACION CPU---------------"+"\nDispositivo: "+str(disp)+"\n"+mdes+" - "+mvar+"\nPromedio: " +str(media)[:5]+ "\nMediana:"+str(mediana)[:5]+"\nDesviación: "+str(desviacion)[:5]+"\nVal. Max:"+str(pico)[:5]+"\n---------------------------------------------------------------"
        if f == True:
            teleg.enviar_mensaje(detalles)




#Pruebas de Funcionamiento
current_dir = os.path.dirname(__file__)
nombreyaml = os.path.join(current_dir, 'inventarios', 'dispositivos.yaml')
datos = obt_infyam.infyam(nombreyaml)
direc = datos.keys()
while True:
    print("Monitoreando CPU")
    datacpu = obt_cpudata(direc)
    warning_cpu(cpuvalref,datacpu)
    time.sleep((cputime+0.5)*60) #Configurado para 30 minutos