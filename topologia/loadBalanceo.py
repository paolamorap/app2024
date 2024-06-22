import yaml
import os

def ordenar_ip(l):
    """
    Permitira ordenadar los pares de conexiones en orden numerico
    Desde la IP mas bajas hasta las mas alta
    l:list  Lista con direcciones IP
    """
    ln = []    
    for i in l:
        ln.append(sorted(i))

    return ln


def eliminar_numeros(lista):
    """
    Función para eliminar los números después del guion en cada elemento de la lista

    lista: list Lista con direcciones IP y sus puertos
    """
    def eliminar_numeros_item(item):
        return tuple(part.split('-')[0] for part in item)

    # Aplicar la función a cada elemento de la lista y devolver el resultado
    return [eliminar_numeros_item(item) for item in lista]

def generar_diccionario_conexiones(vector):
    """
    Función que permite generar diccionarios con las conexiones que tiene cada dispositivo

    vector:list  Lista con tuplas-conexiones
    """
    diccionario_conexiones = {}
    for tupla in vector:
        for direccion in tupla:
            if direccion not in diccionario_conexiones:
                diccionario_conexiones[direccion] = []
        
        # Agregar las conexiones de cada dirección
        diccionario_conexiones[tupla[0]].append(tupla[1])
        diccionario_conexiones[tupla[1]].append(tupla[0])    
    return diccionario_conexiones

def gen_yaml(cone,dispblock,mapint):
    """
    Función para visualizar los puertos que se deben asignar la instancia MSTP
 
    cone:list     Tuplas con conexiones entre dispositivos
    dispblock:    Tupla con direccion IP y el puerto por donde se conecta
    mapint:       Diccionario con el  nombre de las interfaces a configurar
    """
    sal = []
    dic = {}
    tuplas_encontradas = [tupla for tupla in cone if any(elemento in tupla for elemento in dispblock)]
    for tup in tuplas_encontradas:
        ip1 = (tup[0].split("-"))
        ip2 = (tup[1].split("-"))
        return (ip1[0],mapint[ip1[0]][ip1[1]],ip2[0],mapint[ip2[0]][ip2[1]])

def obtener_coincidencia(lista_de_tuplas, direcciones):
    """
    Función para devolver las direcciones con puertos de dos direcciones IP.

    lista_de_tuplas: list       Lista de conexiones/tuplas
    direcciones:list            Lista con par de direcciones IP
    """
    for tupla in lista_de_tuplas:
        if all(direccion in tupla[0].split('-')[0] or direccion in tupla[1].split('-')[0] for direccion in direcciones):
            return tupla
    return None

def obtener_clave(diccionario, lista):
    for clave, valores in diccionario.items():
        if set(lista).issubset(valores):
            return clave
    return None

def conteo_conex(pb,lb,lc,cone,dis,map):
    """
    Funcion que devuelve la información del archivo yaml para configurar las instancias

    pb: Lista con direcciones de los dispositivos que poseen un puerto bloqueado
    
    """
    sal = []
    pbn  = tuple(part.split('-')[0] for part in pb)
    c = 0
    for i in lb:
        if lc.count(i) >=2:
            sal.append([gen_yaml(cone,dis[c],map)])
        else:
            df = generar_diccionario_conexiones(lc)
            ni = obtener_clave(df,i)
            for x in i:
                if x not in pbn:
                    nt = obtener_coincidencia(cone,list([x,ni]))
            sal.append([gen_yaml(cone,dis[c],map),gen_yaml(cone,nt,map)])
        c +=1 

    return sal

def obtener_direcciones_unicas(lista_de_listas):
    direcciones_por_lista = []

    for lista in lista_de_listas:
        direcciones = []
        for tupla in lista:
            direcciones.extend(tupla[::2])  # Seleccionar cada primer elemento de cada tupla
        # Eliminar direcciones duplicadas
        direcciones = str(tuple(set(direcciones)))
        direcciones_por_lista.append(direcciones)

    return direcciones_por_lista


def ob_yaml(lconex, lbl, d):
    """
    Obtener información para el archivo YAML
    lconex: list    Lista de conexiones
    lbl: list       Lista de puertos bloqueados
    d: dict         Diccionario con nombres de interfaces
    """

    lcn = ordenar_ip(eliminar_numeros(lconex))
    lbl1 = [tupla for tupla in lconex if any(elemento in tupla for elemento in lbl)]
    lbln = ordenar_ip(eliminar_numeros(lbl1))
    s = conteo_conex(lbl, lbln, lcn, lconex, lbl1, d)
    dp = obtener_direcciones_unicas(s)

    return s, dp


def yaml_web(dp):
    """
    Genera y escribe un archivo YAML con los enlaces redundantes (direcciones IP de las conexiones).
    Este archivo yaml sera empleado para visualizar los enlaces redundantes en la pagina web. 
    
    Parámetros:
    - dp (list): Lista de enlaces redundantes.
    
    """
    # Crear la estructura de datos para el archivo YAML
    datos_web = {f'enlace{i+1}': f"Enlace {i+1}: {' - '.join(eval(dp[i]))}" for i in range(len(dp))}
    yaml_data = {
        'datos_web': datos_web,
    }

    current_dir = os.path.dirname(__file__)
    segmento_topologiafija = "balanceo/balanceo_web.yaml"
    ruta= os.path.join(current_dir, segmento_topologiafija)

    # Escribir los datos en un archivo YAML
    with open(ruta, 'w') as file:
        yaml.dump(yaml_data, file, default_flow_style=False, sort_keys=False)


def yaml_datos(conexiones):
    """
    Genera y escribe un archivo YAML con los enlaces redundantes (direcciones IP de las conexiones) y 
    sus respectivas interfaces.
    
    Parámetros:
    - conexiones (list): Lista de enlaces redundantes con sus respectivas interfaces. 
    """
    # Diccionario que contendrá todas las conexiones
    conexiones_dict = {'conexiones_disp': {}}
    # Iterar sobre cada grupo de conexiones
    for idx, grupo in enumerate(conexiones, start=1):
        conexion_key = f'enlace{idx}'
        conexiones_dict['conexiones_disp'][conexion_key] = {}
        host_index = 1
        # Iterar sobre cada conexión individual en el grupo
        for host_info in grupo:
            ip, interfaz, ip_destino, interfaz_destino = host_info
            host_key = f'host{host_index}'
            host_index += 1
            conexiones_dict['conexiones_disp'][conexion_key][host_key] = {
                'IP': ip,
                'interfaz1': interfaz
            }
            host_key = f'host{host_index}'
            host_index += 1
            conexiones_dict['conexiones_disp'][conexion_key][host_key] = {
                'IP': ip_destino,
                'interfaz1': interfaz_destino
            }
    # Escribir el diccionario a un archivo YAML
    current_dir = os.path.dirname(__file__)
    segmento_topologiafija = "balanceo/balanceo_datos.yaml"
    ruta= os.path.join(current_dir, segmento_topologiafija)

    with open(ruta, 'w') as file:
        yaml.dump(conexiones_dict, file, sort_keys=False, default_flow_style=False)