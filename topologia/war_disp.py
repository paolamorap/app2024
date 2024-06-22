from collections import deque
from collections import defaultdict
import time
import tree
import teleg
from influxdb import InfluxDBClient
import loadBalanceo
import networkx as nx
import obt_infyam
import os
#Valores de configuración del script
current_dir = os.path.dirname(__file__)
config_file = current_dir+'/configuracion/configuracion_monitoreo.json'
config = obt_infyam.read_config(config_file)
time_int = config.get('wartiempointe', 10)  
num_int = config.get('warnuminte', 5)  

with open('datos.txt', 'r') as archivo:
    time_mon = str(archivo.readline().strip())

def ip_to_tuple(ip):
    return tuple(map(int, ip.split('.')))

def encontrar_caminos_posibles(grafo_matriz, nodo_inicial, nodo_final):
    """
    Funcion que permite encontrar los caminos entre dos nodos

    Parameters:
    grafo_matriz(matriz):   Representación del Grafo a través de una matriz
    nodo_inicial(int):      Nodo Inicial
    nodo_final(int):        Nodo Final

    Return:
    caminos_posibles(list): Lista con los nodos que conforman el camino entre los nodos
    """
    # Convertir la matriz de adyacencia en un grafo dirigido
    G = nx.DiGraph()
    for i in range(len(grafo_matriz)):
        for j in range(len(grafo_matriz[i])):
            if grafo_matriz[i][j] == 1:
                G.add_edge(i, j)

    # Encontrar todos los caminos posibles entre nodo_inicial y nodo_final
    caminos_posibles = list(nx.all_simple_paths(G, source=nodo_inicial, target=nodo_final))

    return caminos_posibles


# Configurar la conexión a la base de datos InfluxDB
client = InfluxDBClient(host='127.0.0.1', port=8086, database='influx')

def leer_incidencias(agentes):
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
        query = f'SELECT sum("interrupciones") FROM "interrumpciones" WHERE ("dispositivo" = \'{agente}\') AND time >= now() -  {time_int}m and time <= now() GROUP BY time(168h) fill(null);'
        # Ejecutar la consulta para el agente actual
        result = client.query(query)
        for point in result.get_points():
            infcpuconsum[agente] = (float(point["sum"]))

    # Cerrar la conexión
    client.close()
    return infcpuconsum

def grafo_a_matriz(grafo):
    """
    Permite convertir un diccionario que posee información de un grafo a su representación
    en matriz

    Parameters:
    grafo(dict):    Diccionario con las conexiones adyacentes de cada dispositivo

    Returns:
    matriz(matriz)  Representación del grafo en forma de matriz
    """
    # Obtener todos los nodos únicos del grafo
    nodos = sorted(set(grafo.keys()))

    # Inicializar una matriz cuadrada de ceros del tamaño adecuado
    n = len(nodos)
    matriz = [[0] * n for _ in range(n)]

    # Llenar la matriz con las conexiones del grafo
    for i, nodo in enumerate(nodos):
        for vecino in grafo[nodo]:
            j = nodos.index(vecino)
            matriz[i][j] = 1

    return matriz

def iden_disp_conec(conex,interconexiones,root):
    """
    Función que permite identificar los dispositivos conectados serie

    Parameters:
    conex(dict):            Diccionario con tuplas que representan las conexiones del arbol
    interconexiones(dict):  Diccionario con tuplas que representan las conexiones del arbol
    Contiene el nombre de las interfaces que se conectan
    root(str):              Dirección IP del switch Root
    
    Return:
    conexf(dict):   Cntiene un diccionario que posee como clave la direccion IP de un switch y como valores
    una lista con las conexiones que dependen de ese dispositivo
    """
    conex_prevencion = {}
    eqmatriz= {}
    reqmatriz= {}
    conexf = {}
    saltos = {}
    lcn = (loadBalanceo.ordenar_ip(loadBalanceo.eliminar_numeros(conex)))
    conex =  loadBalanceo.generar_diccionario_conexiones(lcn)
    a = []
    c = 0
    lj = []
    direc1 = list(conex.keys())
    direc = sorted(direc1, key=ip_to_tuple)
    conjunto_resultante = set()
    maconex = grafo_a_matriz(conex)
    #Calculo de niveles de los dispositivos
    for disp in direc:
        saltos[disp] = tree.calcular_saltos(interconexiones,root,disp)
    
    #Mapeo de indices de matriz a direcciones IP
    for aux in direc:
        eqmatriz[aux] = c
        reqmatriz[c] = aux
        c +=1

    for di in direc:
        a = []
        nr = saltos[di] #Nivel de referencia
        lj = []
        lista_resultante = []
        for lim in direc:
            if di !=lim:
                    f = True
                    aux = encontrar_caminos_posibles(maconex,eqmatriz[di],eqmatriz[lim])
                    for cx in aux[0]:
                        nv = saltos[reqmatriz[cx]]
                        if nv< nr:
                            f = False
                            break
                    if f:
                        a += encontrar_caminos_posibles(maconex,eqmatriz[di],eqmatriz[lim])
        conjunto_resultante = set([])
        for lista in a:
            conjunto_resultante |= set(lista)
        # Convertir el conjunto resultante de nuevo en una lista
        lista_resultante = list(conjunto_resultante)
        conex_prevencion[di] = lista_resultante


    for ips in direc:
        nr = saltos[ips] #Nivel de referencia
        lj = []
        for cam in conex_prevencion[ips]:
            ip2 = reqmatriz[cam]
            nv = saltos[ip2]#Nivel Vecino

            if nv > nr and ips != ip2:
                lj.append(ip2) 

        conexf[ips] = lj
    return conexf

def prevención_corte(direc,dic_conex):
    """
    Funcion para emitir advertencia preventiva en caso de que un switch falle

    Parameters:
    conexiones(list):       Lista con tuplas que especifican las conexiones entre dispositivos
    root(str):              Dirección IP de la raíz del árbol STP 


    Returns:
    Advertencia - Mensaje enviado por telegram
    """
    interrupciones = leer_incidencias(direc)
    #Generar Advertencia
    cabecera = "-----------------------Notificación---------------------------"
    tail = "-"*len(cabecera)
    for disp in direc:
        mes = ""
        mesf = ""
        if  interrupciones[disp] >= num_int:
            for di in dic_conex[disp]:
                mes += str(di)+"\n"
            mesf = (cabecera+"\nMúltiples Interrupciones en: "+disp+"\n Posibles dispositivos afectados: \n"
                  + mes+"\n"+tail)
            
            print(mesf)
            teleg.enviar_mensaje(mesf)


while True:
    print("Monitoreando Interrupciones - Prevenciones de Enlaces")
    with open('datos.txt', 'r') as archivo:
        direc = eval(archivo.readline().strip())
        l = eval(archivo.readline().strip())
        interconections = eval(archivo.readline().strip())
        broot =  str(archivo.readline().strip())
        dic_cone = iden_disp_conec(l,interconections,broot)
        prevención_corte(direc,dic_cone)
    time.sleep(time_int*60)