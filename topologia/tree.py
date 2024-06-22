import json
import yaml
import os
import re
from collections import deque
from pysnmp.hlapi import getCmd, CommunityData, UdpTransportTarget, SnmpEngine, ContextData, ObjectType, ObjectIdentity

def generar_arbol_conexiones_web(interconexiones, info_puertos):
    """
    Genera una lista de conexiones entre dispositivos basada en la información de interconexiones y puertos.

    Parámetros:
    - interconexiones (list): Lista de tuplas que representan conexiones entre dispositivos. Cada conexión se representa como
                              una tupla de dos cadenas 'dispositivo-puerto', por ejemplo, '192.168.20.1-1'.
    - info_puertos (dict): Diccionario que mapea identificadores de dispositivos a diccionarios de puertos, donde cada puerto
                           se mapea a su nombre correspondiente.

    Retorna:
    - list: Lista de conexiones, donde cada conexión es una lista de dos tuplas. Cada tupla contiene la IPdel dispositivo
            y el nombre del puerto correspondiente, facilitando la visualización y gestión de conexiones en aplicaciones web.

    Esta función recorre la lista de interconexiones, descompone las cadenas de conexión en dispositivo y puerto, y utiliza el
    diccionario `info_puertos` para obtener nombres de puertos humanamente legibles. Solo se incluyen en la lista final aquellas
    conexiones donde ambos nombres de puerto están disponibles.
    """
    conexiones = []
    for conexion in interconexiones:
        dispositivo_origen, puerto_origen = conexion[0].split('-')
        dispositivo_destino, puerto_destino = conexion[1].split('-')

        nombre_puerto_origen = info_puertos.get(dispositivo_origen, {}).get(puerto_origen)
        nombre_puerto_destino = info_puertos.get(dispositivo_destino, {}).get(puerto_destino)
        
        # Añadir la conexión a la lista si se encontraron nombres válidos para ambos puertos
        if nombre_puerto_origen and nombre_puerto_destino:
            conexiones.append([
                #(dispositivo_origen, nombre_puerto_origen),
                #(dispositivo_destino, nombre_puerto_destino)
                (f'{dispositivo_origen}', nombre_puerto_origen),
                (f'{dispositivo_destino}', nombre_puerto_destino)
            ])

    return conexiones


def identificar_interfaces_bloqueadas(bloqueos, interfaces):
    """
    Identifica y lista las interfaces que están bloqueadas según los datos proporcionados.

    Parámetros:
    - bloqueos (list): Lista de identificadores de bloqueo en formato 'IP-interfaz_numero' (ejemplo, '192.168.1.1-1').
    - interfaces (dict): Diccionario donde cada clave es una dirección IP y cada valor es otro diccionario.
                         Este subdiccionario tiene números de interfaz como claves y nombres de interfaz como valores.

    Retorna:
    - list: Lista de tuplas, donde cada tupla contiene la IP y el nombre de la interfaz que está bloqueada.

    Esta función procesa una lista de identificadores de bloqueo y un diccionario de interfaces para determinar
    cuáles de estas interfaces están efectivamente bloqueadas. Devuelve una lista de las interfaces identificadas
    como bloqueadas, facilitando la gestión de la red y la resolución de problemas relacionados con bloqueos.
    """
    interfaces_bloqueadas = []
    for bloqueo in bloqueos:
        ip, numero_interfaz = bloqueo.split('-')  # Descompone el identificador de bloqueo en IP y número de interfaz
        # Comprobar si la IP y el número de interfaz existen en el diccionario de interfaces
        if ip in interfaces and numero_interfaz in interfaces[ip]:
            nombre_interfaz = interfaces[ip][numero_interfaz]
            interfaces_bloqueadas.append((ip, nombre_interfaz))  # Agregar a la lista como tupla

    return interfaces_bloqueadas


def marcar_puertos_bloqueados(conexiones, puertos_bloqueados):
    """
    Marca los puertos especificados como bloqueados en la lista de conexiones proporcionada.

    Parámetros:
    - conexiones (list): Lista de listas de tuplas, donde cada tupla representa una conexión individual (IP, puerto).
    - puertos_bloqueados (list): Lista de tuplas (IP, puerto) que deben ser marcadas como bloqueadas.

    Retorna:
    - list: Una lista de listas de tuplas, donde cada tupla incluye un indicador de si el puerto está bloqueado (True/False).

    Esta función recorre la lista de conexiones y añade un tercer elemento a cada tupla dentro de las sublistas,
    indicando si esa conexión (IP, puerto) está dentro del conjunto de puertos bloqueados. Utiliza un conjunto
    para los puertos bloqueados para mejorar la eficiencia de las búsquedas.
    """
    # Convertir la lista de puertos bloqueados en un conjunto para búsquedas más eficientes
    conjunto_puertos_bloqueados = set(puertos_bloqueados)
    
    # Nueva lista para almacenar conexiones con el indicador de bloqueo
    conexiones_marcadas = []
    
    for conexion in conexiones:
        conexion_actualizada = []
        for ip, puerto in conexion:
            # Agregar el estado de bloqueo a la tupla
            conexion_actualizada.append((ip, puerto, (ip, puerto) in conjunto_puertos_bloqueados))
        conexiones_marcadas.append(conexion_actualizada)
    return conexiones_marcadas



def calcular_saltos(topologia_red, nodo_origen, nodo_destino):
    """
    Calcula el número de saltos mínimos entre dos nodos en una red utilizando el algoritmo de búsqueda en anchura (BFS).

    Parámetros:
    - topologia_red (list): Lista de tuplas que representan las conexiones entre dispositivos en la red.
    - nodo_origen (str): El nodo de origen desde el cual comenzar la búsqueda.
    - nodo_destino (str): El nodo destino al cual se desea llegar.

    Retorna:
    - int: El número mínimo de saltos necesarios para ir del origen al destino. Si los nodos son iguales,
           se devuelve 1, indicando que el nodo destino es el mismo que el origen. Si no existe camino, se devuelve 0.

    Esta función construye un grafo no dirigido a partir de la topología de la red y luego realiza una búsqueda
    en anchura para encontrar la ruta más corta entre el nodo origen y el nodo destino, contando los saltos necesarios.
    """
    if nodo_origen == nodo_destino:  # Si el origen y el destino son iguales, devolver 1 salto
        return 1
    
    # Crear un grafo a partir de las conexiones de la red
    grafo = {}
    for conexion in topologia_red:
        dispositivo_a, _ = conexion[0]
        dispositivo_b, _ = conexion[1]
        if dispositivo_a not in grafo:
            grafo[dispositivo_a] = []
        if dispositivo_b not in grafo:
            grafo[dispositivo_b] = []
        grafo[dispositivo_a].append(dispositivo_b)
        grafo[dispositivo_b].append(dispositivo_a)
    
    # Realizar la búsqueda en anchura (BFS)
    visitados = set()
    cola = deque([(nodo_origen, 0)])  # Tupla de (dispositivo, saltos)
    while cola:
        dispositivo_actual, saltos = cola.popleft()
        if dispositivo_actual == nodo_destino:
            return saltos + 1
        visitados.add(dispositivo_actual)
        for vecino in grafo.get(dispositivo_actual, []):
            if vecino not in visitados:
                cola.append((vecino, saltos + 1))
    return 0  # No se encontró un camino

def obtener_hostname_dispositivos(ips, datos):
    """
    Realiza consultas SNMP para obtener los nombres de host de una lista de direcciones IP.

    Parámetros:
    - ips (list): Lista de direcciones IP de los dispositivos a consultar.
    - datos (dict): Diccionario que contiene la información SNMP para cada IP, incluyendo la comunidad.

    Retorna:
    - dict: Un diccionario donde cada clave es una dirección IP y cada valor es otro diccionario que contiene el 'host_name'
            obtenido. Si el nombre de host no se puede obtener debido a errores SNMP o de otro tipo, se devolverá None para ese host.

    La función utiliza la librería SNMP para hacer consultas y extraer el nombre de host (sysName) de cada dispositivo.
    Usa expresiones regulares para extraer la parte relevante del nombre de host si es necesario.
    """
    hostname_dispositivos = {}
    for ip_servidor in ips:
        comunidad = datos[ip_servidor]["snmp"]
        info_temporal = {'host_name': None}
        
        # Realizar la consulta SNMP para obtener el nombre de host
        errorIndicacion, errorEstado, errorIndice, varBinds = next(
            getCmd(
                SnmpEngine(),
                CommunityData(comunidad),
                UdpTransportTarget((ip_servidor, 161)),
                ContextData(),
                ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0'))
            )
        )
        if not errorIndicacion and not errorEstado and varBinds:
            nombre_completo = varBinds[0][1].prettyPrint()
            # Extraer la parte antes del primer punto usando expresiones regulares
            coincidencia = re.match(r"([^\.]+)", nombre_completo)
            if coincidencia:
                info_temporal['host_name'] = coincidencia.group(1)
            else:
                info_temporal['host_name'] = nombre_completo  # Usar el nombre de host completo si no hay punto
        
        # Almacenar los resultados para esta IP
        hostname_dispositivos[ip_servidor] = info_temporal

    return hostname_dispositivos



def informacion_dispositivos(nombre_archivo):
    """
    Carga y procesa la información de dispositivos de un archivo YAML para mapear IPs a sus respectivos tipos y marcas.

    Parámetros:
    - nombre_archivo (str): La ruta del archivo YAML que contiene la información de los dispositivos.

    Retorna:
    - dict: Un diccionario donde cada clave es una dirección IP de un dispositivo y cada valor es otro
            diccionario que contiene el 'tipo' y la 'marca' de ese dispositivo, denominado `datos_dispositivos`.

    La función abre y lee un archivo YAML que se espera contenga un grupo de dispositivos, cada uno con su tipo y marca.
    Procesa este archivo para crear un diccionario mapeando cada IP a su información correspondiente de tipo y marca.
    Esta información es útil para operaciones de red que necesitan identificar dispositivos por tipo o marca.
    """
    # Carga los datos del archivo YAML
    with open(nombre_archivo, "r") as archivo:
        datos_yaml = yaml.safe_load(archivo)
    
    datos_dispositivos = {}
    
    # Procesa cada grupo de dispositivos en el archivo YAML
    for grupo in datos_yaml:
        tipo = datos_yaml[grupo]['vars'].get('tipo')
        marca = datos_yaml[grupo]['vars'].get('marca')

        # Itera sobre cada host en el grupo y extrae la información relevante
        for host, config in datos_yaml[grupo]['hosts'].items():
            ip = config['host']  # Obtiene la IP correctamente
            info_temporal = {'tipo': tipo, 'marca': marca}  # Crea un diccionario para cada host
            datos_dispositivos[ip] = info_temporal
            
    return datos_dispositivos


def generar_topologia_fija(*args):
    """
    Genera un diccionario que representa la topología de red fija basada en varios parámetros de entrada.

    Parámetros:
    - args (tuple): Una tupla que contiene:
        1. discovered_hosts (list): Lista de hosts descubiertos.
        2. interconnections (dict): Diccionario de interconexiones.
        3. b_root (str): Identificador del host raíz.
        4. conexiones_blk (list): Lista de conexiones bloqueadas.
        5. host_name_dict (dict): Diccionario de nombres de hosts.
        6. info_disp (dict): Diccionario de información de dispositivos (marca, modelo, tipo).

    Retorna:
    - dict: Un diccionario con dos listas, 'nodes' y 'links', que representan los nodos y enlaces de la topología.

    La función procesa los hosts descubiertos y sus conexiones para crear una estructura de datos que describe 
    los nodos y enlaces en la topología, incluyendo detalles como nombres de dispositivos, tipos, y 
    conexiones interdispositivos, así como la gestión de conexiones bloqueadas.
    """
    hosts_descubiertos, interconexiones, host_raiz, conexiones_bloqueadas, dict_nombres_hosts, info_dispositivos = args
    id_host = 0
    origen = host_raiz
    mapa_id_host = {}
    dict_topologia = {'nodes': [], 'links': []}
    enlaces_por_pares = {}
    
    # Procesa cada host descubierto y construye la lista de nodos
    for host in hosts_descubiertos:
        mapa_id_host[host] = id_host
        nombre_host_actual = dict_nombres_hosts.get(host, {}).get('host_name', 'Nombre desconocido')
        marca_modelo = info_dispositivos.get(host, {}).get('marca', 'Marca/Modelo desconocido')
        tipo_dispositivo = info_dispositivos.get(host, {}).get('tipo', 'switch')
        
        dict_topologia['nodes'].append({
            'icon': tipo_dispositivo,
            'id': id_host,
            'name': nombre_host_actual,
            'IP': host,
            'marca': marca_modelo,
            'layerSortPreference': calcular_saltos(interconexiones, origen, host),
        })
        id_host += 1
    
    # Procesa las conexiones bloqueadas para construir la lista de enlaces
    id_enlace = 0
    for conexion in conexiones_bloqueadas:
        src, tgt = conexion[0][0], conexion[1][0]
        bloqueo_src, bloqueo_tgt = conexion[0][2], conexion[1][2]
        clave_par = tuple(sorted([src, tgt]))
        
        if clave_par not in enlaces_por_pares:
            enlaces_por_pares[clave_par] = 0
        enlaces_por_pares[clave_par] += 1
        
        indice = enlaces_por_pares[clave_par]
        dict_topologia['links'].append({
            'id': id_enlace,
            'source': mapa_id_host[src],
            'target': mapa_id_host[tgt],
            'srcIfName': conexion[0][1],
            'srcDevice': src,
            'port_bloks': bloqueo_src,
            'tgtIfName': conexion[1][1],
            'tgtDevice': tgt,
            'port_blokt': bloqueo_tgt,
            'index': indice,
        })
        id_enlace += 1

    return dict_topologia


def guardar_archivo_topologia(topologia_json, encabezado, destino):
    """
    Guarda la topología de red en un archivo, incluyendo un encabezado personalizado y un formato específico.

    Parámetros:
    - topologia_json (dict): La topología de red que se desea guardar, representada como un diccionario.
    - encabezado (str): Un texto de encabezado que se incluirá al principio del archivo.
    - destino (str): Ruta del archivo de destino donde se guardará la topología en formato JSON.

    La función escribe un encabezado personalizado seguido de la topología de red formateada en JSON,
    y finaliza con un punto y coma. Este formato puede ser útil para aplicaciones que necesiten leer el archivo
    con un formato específico o para delimitar el contenido del archivo de manera clara.

    Nota: Si ocurre un error durante la apertura o escritura del archivo, el error será manejado por la
    gestión de excepciones implícita en el entorno de ejecución.
    """
    # Abre el archivo de destino en modo escritura
    with open(destino, 'w') as archivo_topologia:
        # Escribe el encabezado al archivo
        archivo_topologia.write(encabezado)
        # Escribe la topología en formato JSON, con indentación y claves ordenadas
        archivo_topologia.write(json.dumps(topologia_json, indent=4, sort_keys=True))
        # Agrega un punto y coma al final como delimitador
        archivo_topologia.write(';')

def guardar_topologia_cache(topologia_json, destino):
    """
    Guarda la topología de red especificada en un archivo JSON.

    Parámetros:
    - topologia_json (dict): La topología de red que se desea guardar, representada como un diccionario.
    - destino (str): Ruta del archivo de destino donde se guardará la topología en formato JSON.

    Esta función escribe la topología de red proporcionada en un archivo JSON, formateando el contenido
    con indentación para mejorar la legibilidad y ordenando las claves. Esto facilita la visualización
    y el mantenimiento del archivo JSON. Si ocurre un error durante el proceso de escritura, el error
    será manejado por la gestión de excepciones implícita en el entorno de ejecución.
    """
    # Abre el archivo de destino en modo escritura
    with open(destino, 'w') as archivo_destino:
        # Escribe la topología en formato JSON, con indentación y claves ordenadas
        archivo_destino.write(json.dumps(topologia_json, indent=4, sort_keys=True))


def leer_topologia_cache(nombre_archivo):
    """
    Lee y carga la topología de red guardada en un archivo JSON.

    Parámetros:
    - nombre_archivo (str): La ruta del archivo donde está guardada la topología de red en formato JSON.

    Retorna:
    - dict: Un diccionario que representa la topología de red cargada desde el archivo.
    - dict vacío ({}): Si el archivo no existe, no es un archivo o ocurre un error al leer el archivo.

    Esta función verifica primero si el archivo especificado existe y es un archivo regular. Si es así,
    intenta abrir y leer el archivo para cargar la topología de red. Si ocurre algún error durante la
    lectura o el archivo no cumple con las condiciones, retorna un diccionario vacío.
    """
    # Verifica si el archivo existe y es un archivo regular
    if not os.path.exists(nombre_archivo) or not os.path.isfile(nombre_archivo):
        return {}

    # Intenta leer y cargar la topología desde el archivo
    topologia_cacheada = {}
    with open(nombre_archivo, 'r') as archivo:
        try:
            topologia_cacheada = json.loads(archivo.read())
        except:
            return {}
    return topologia_cacheada


def generar_topologia_diferencias(topologia_almacenada, topologia_actual):
    """
    Genera las diferencias entre dos topologías de red, identificando nodos y enlaces añadidos o eliminados.

    Parámetros:
    - topologia_almacenada (dict): Topología previamente almacenada, con nodos y enlaces.
    - topologia_actual (dict): Topología actual de la red, con nodos y enlaces.

    Retorna:
    - tuple: Contiene tres elementos:
        1. Diccionario de nodos añadidos y eliminados.
        2. Diccionario de enlaces añadidos y eliminados.
        3. Diccionario con la topología combinada y actualizada.
    """
    
    diferencias_nodos = {'added': [], 'deleted': []}
    diferencias_enlaces = {'added': [], 'deleted': []}
    topologia_combinada = {'nodes': [], 'links': []}
    
    enlaces_almacenados = [(link, ((link['srcDevice'], link['srcIfName']), (link['tgtDevice'], link['tgtIfName'])))
                           for link in topologia_almacenada['links']]
    enlaces_actuales = [(link, ((link['srcDevice'], link['srcIfName']), (link['tgtDevice'], link['tgtIfName'])))
                        for link in topologia_actual['links']]
    nodos_almacenados = [(node, (node['IP'],)) for node in topologia_almacenada['nodes']]
    nodos_actuales = [(node, (node['IP'],)) for node in topologia_actual['nodes']]
    
    id_nodo = 0
    mapa_id_host = {}
    for datos_nodo, nodo in nodos_actuales:
        if nodo not in [n[1] for n in nodos_almacenados]:
            diferencias_nodos['added'].append(nodo)
            datos_nodo['id'] = id_nodo
            mapa_id_host[datos_nodo['IP']] = id_nodo
            datos_nodo['is_new'] = 'yes'
            datos_nodo['is_dead'] = 'no'
            topologia_combinada['nodes'].append(datos_nodo)
            id_nodo += 1
        else:
            datos_nodo['id'] = id_nodo
            mapa_id_host[datos_nodo['IP']] = id_nodo
            datos_nodo['is_new'] = 'no'
            datos_nodo['is_dead'] = 'no'
            topologia_combinada['nodes'].append(datos_nodo)
            id_nodo += 1
            
    for datos_nodo, nodo_almacenado in nodos_almacenados:
        if nodo_almacenado not in [n[1] for n in nodos_actuales]:
            diferencias_nodos['deleted'].append(nodo_almacenado)
            datos_nodo['id'] = id_nodo
            mapa_id_host[datos_nodo['IP']] = id_nodo
            datos_nodo['is_new'] = 'no'
            datos_nodo['is_dead'] = 'yes'
            datos_nodo['icon'] = 'dead_node'
            topologia_combinada['nodes'].append(datos_nodo)
            id_nodo += 1
    
    id_enlace = 0
    for datos_enlace, enlace in enlaces_actuales:
        src, dst = enlace
        if (src, dst) not in [e[1] for e in enlaces_almacenados] and (dst, src) not in [e[1] for e in enlaces_almacenados]:
            diferencias_enlaces['added'].append((src, dst))
            datos_enlace['id'] = id_enlace
            datos_enlace['source'] = mapa_id_host[src[0]]
            datos_enlace['target'] = mapa_id_host[dst[0]]
            datos_enlace['is_new'] = 'yes'
            datos_enlace['is_dead'] = 'no'
            topologia_combinada['links'].append(datos_enlace)
            id_enlace += 1
        else:
            datos_enlace['id'] = id_enlace
            datos_enlace['source'] = mapa_id_host[src[0]]
            datos_enlace['target'] = mapa_id_host[dst[0]]
            datos_enlace['is_new'] = 'no'
            datos_enlace['is_dead'] = 'no'
            topologia_combinada['links'].append(datos_enlace)
            id_enlace += 1
            
    for datos_enlace, enlace in enlaces_almacenados:
        src, dst = enlace
        if (src, dst) not in [e[1] for e in enlaces_actuales] and (dst, src) not in [e[1] for e in enlaces_actuales]:
            diferencias_enlaces['deleted'].append((src, dst))
            datos_enlace['id'] = id_enlace
            datos_enlace['source'] = mapa_id_host[src[0]]
            datos_enlace['target'] = mapa_id_host[dst[0]]
            datos_enlace['is_new'] = 'no'
            datos_enlace['is_dead'] = 'yes'
            topologia_combinada['links'].append(datos_enlace)
            id_enlace += 1

    return diferencias_nodos, diferencias_enlaces, topologia_combinada


def imprimir_diferencias(diff_result):
    """
    Imprime las diferencias en la topología de red detectadas entre ejecuciones.

    Esta función analiza los resultados de las diferencias en la topología de red, 
    identificando dispositivos y conexiones añadidos o eliminados. Es útil para
    monitorear cambios en una infraestructura de red y tomar acciones basadas en estos cambios.

    Parámetros:
    - diff_result (tuple): Una tupla que contiene diccionarios de nodos y enlaces añadidos y eliminados.

    Retorna:
    - None: La función solo imprime los resultados, no retorna valores.
    """
    # Extracción de resultados de diferencias en nodos y enlaces
    diff_nodes, diff_links, *ignore = diff_result

    # Verificación de la presencia de cambios
    if not (diff_nodes['added'] or diff_nodes['deleted'] or diff_links['added'] or diff_links['deleted']):
        print('No hubo cambios en la topología desde la última ejecución.')
        return

    print('Se han descubierto cambios en la topología:')
    # Procesamiento e impresión de nodos añadidos
    if diff_nodes['added']:
        print('\n^^^^^^^^^^^^^^^^^^^^')
        print('Nuevos dispositivos de red:')
        print('vvvvvvvvvvvvvvvvvvvv')
        for node in diff_nodes['added']:
            print(f'Hostname: {node[0]}')

    # Procesamiento e impresión de nodos eliminados
    if diff_nodes['deleted']:
        print('\n^^^^^^^^^^^^^^^^^^^^^^^^')
        print('Dispositivos de red eliminados:')
        print('vvvvvvvvvvvvvvvvvvvvvvvv')
        for node in diff_nodes['deleted']:
            print(f'Hostname: {node[0]}')

    # Procesamiento e impresión de enlaces añadidos
    if diff_links['added']:
        print('\n^^^^^^^^^^^^^^^^^^^^^^')
        print('Nuevas interconexiones:')
        print('vvvvvvvvvvvvvvvvvvvvvv')
        for src, dst in diff_links['added']:
            print(f'De {src[0]}({src[1]}) a {dst[0]}({dst[1]})')

    # Procesamiento e impresión de enlaces eliminados
    if diff_links['deleted']:
        print('\n^^^^^^^^^^^^^^^^^^^^^^^^^')
        print('Interconexiones eliminadas:')
        print('vvvvvvvvvvvvvvvvvvvvvvvvv')
        for src, dst in diff_links['deleted']:
            print(f'De {src[0]}({src[1]}) a {dst[0]}({dst[1]})')
    print('')