import json
import yaml
from collections import deque
from collections import defaultdict
import os

from pysnmp.hlapi import getCmd, CommunityData, UdpTransportTarget, SnmpEngine, ContextData, ObjectType, ObjectIdentity
import re

icon_capability_map = {
    'router': 'router',
    'switch': 'switch',
    'bridge': 'switch',
    'station': 'host'
}

def generate_switch_names(ip_addresses):
    switches =  [ip for ip in ip_addresses]
    return switches

def connection_tree_web(interconnections, port_info):
    connections = []
    for connection in interconnections:
        source_switch, source_port = connection[0].split('-')
        target_switch, target_port = connection[1].split('-')

        source_port_name = port_info.get(source_switch, {}).get(source_port)
        target_port_name = port_info.get(target_switch, {}).get(target_port)
        
        if source_port_name and target_port_name:
            connections.append([
                (f'{source_switch}', source_port_name),
                (f'{target_switch}', target_port_name)
            ])

    return connections

def identificar_interfaces_bloqueadas(bloqueos, interfaces):
    interfaces_bloqueadas = []
    for bloqueo in bloqueos:
        ip, interfaz_numero = bloqueo.split('-')
        if ip in interfaces and interfaz_numero in interfaces[ip]:
            nombre_interfaz = interfaces[ip][interfaz_numero]
            interfaces_bloqueadas.append((ip, nombre_interfaz))
    return interfaces_bloqueadas

def marcar_puertos_bloqueados(conexiones, puertos_bloqueados):
    # Convertir la lista de puertos bloqueados en un conjunto para búsquedas más eficientes
    puertos_bloqueados_set = set(puertos_bloqueados)
    
    # Nueva lista para almacenar conexiones con el indicador de bloqueo
    conexiones_blok = []
    
    for conexion in conexiones:
        conexion_actualizada = []
        for ip, puerto in conexion:
            # Agregar el estado de bloqueo a la tupla
            conexion_actualizada.append((ip, puerto, (ip, puerto) in puertos_bloqueados_set))
        conexiones_blok.append(conexion_actualizada)
    return conexiones_blok

def get_icon_type(device_cap_name, device_model=''):
    if device_cap_name:
        icon_type = icon_capability_map.get(device_cap_name)
        if icon_type:
            return icon_type
    return 'unknown'

def calcular_saltos(red, origen, destino):
    if origen == destino:  # Si el origen y el destino son iguales, devolver 0 saltos
        return 1
    
    # Crear un grafo a partir de las conexiones de la red
    grafo = {}
    for conexion in red:
        dispositivo_a, puerto_a = conexion[0]
        dispositivo_b, puerto_b = conexion[1]
        if dispositivo_a not in grafo:
            grafo[dispositivo_a] = []
        if dispositivo_b not in grafo:
            grafo[dispositivo_b] = []
        grafo[dispositivo_a].append(dispositivo_b)
        grafo[dispositivo_b].append(dispositivo_a)
    
    # Realizar la búsqueda en anchura (BFS)
    visitados = set()
    cola = deque([(origen, 0)])  # Tupla de (dispositivo, saltos)
    while cola:
        dispositivo, saltos = cola.popleft()
        if dispositivo == destino:
            return saltos+1
        visitados.add(dispositivo)
        for vecino in grafo.get(dispositivo, []):
            if vecino not in visitados:
                cola.append((vecino, saltos + 1))
    return 0  # No se encontró un camino

def obtener_hostname_dispositivos(ips, datos):
    resultados = {}
    for server_ip in ips:
        comunidad = datos[server_ip]["snmp"]
        # Diccionario temporal para almacenar los resultados de esta IP
        info_temp = {'host_name': None}
        
        # Obtener el Host Name (sysName)
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(
                SnmpEngine(),
                CommunityData(comunidad),
                UdpTransportTarget((server_ip, 161)),
                ContextData(),
                ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0'))
            )
        )
        if not errorIndication and not errorStatus and varBinds:
            full_hostname = varBinds[0][1].prettyPrint()
            # Utilizar expresión regular para extraer la parte antes del primer punto
            match = re.match(r"([^\.]+)", full_hostname)
            if match:
                info_temp['host_name'] = match.group(1)
            else:
                info_temp['host_name'] = full_hostname  # Usar el hostname completo si no se encuentra un punto
        
        # Almacenar los resultados
        resultados[server_ip] = info_temp

    return resultados


def informacion_dispositivos(nombre):
    with open(nombre, "r") as archivo:
           datos_yaml = yaml.safe_load(archivo)
    
    resultado = {}
    
    for grupo in datos_yaml:
        tipo = datos_yaml[grupo]['vars'].get('tipo')
        marca = datos_yaml[grupo]['vars'].get('marca')

        for host, config in datos_yaml[grupo]['hosts'].items():
            ip = config['host']  # Obtiene la IP correctamente
            info_temp = {'tipo': tipo, 'marca': marca}  # Crea un nuevo diccionario para cada host
            resultado[ip] = info_temp
            
    return resultado  

def generar_topologia_fija(*args):
    discovered_hosts, interconnections, b_root, conexiones_blk, host_name_dict, info_disp = args
    host_id = 0
    origen = b_root
    host_id_map = {}
    topology_dict = {'nodes': [], 'links': []}
    enlaces_entre_pares = {}
    
    for host in discovered_hosts:
        host_id_map[host] = host_id
        current_host_name = host_name_dict.get(host, {}).get('host_name', 'Nombre desconocido')
        marca_modelo = info_disp.get(host, {}).get('marca', 'Marca/Modelo desconocido')
        tipo = info_disp.get(host, {}).get('tipo', 'switch')
        name = f"{current_host_name}"
        marca = f"{marca_modelo}"
        icono = f"{tipo}"

        topology_dict['nodes'].append({
            'icon': icono,
            'id': host_id,
            'name': name,
            'IP': host,
            'marca': marca,
            'layerSortPreference':  calcular_saltos(interconnections, origen, host),
        })
        host_id += 1
    
    link_id = 0
    for link in conexiones_blk:
        src, tgt = link[0][0], link[1][0]
        bloq_s, blok_t = link[0][2], link[1][2]
        par_clave = tuple(sorted([src, tgt]))
        if par_clave not in enlaces_entre_pares:
            enlaces_entre_pares[par_clave] = 0
        enlaces_entre_pares[par_clave] += 1
        index = enlaces_entre_pares[par_clave]
        topology_dict['links'].append({
            'id': link_id,
            'source': host_id_map[src],
            'target': host_id_map[tgt],
            'srcIfName': link[0][1],
            'srcDevice': src,
            'port_bloks': bloq_s,
            'tgtIfName': link[1][1],
            'tgtDevice': tgt,
            'port_blokt': blok_t,
            'index': index,
        })
        link_id += 1

    return topology_dict

# Función auxiliar si_shortname
def if_shortname(interface):
    return interface

def guardar_archivo_topologia(topology_json, header, dst):
    with open(dst, 'w') as topology_file:
        topology_file.write(header)
        topology_file.write(json.dumps(topology_json, indent=4, sort_keys=True))
        topology_file.write(';')


#*********************************************************************************************************************

def guardar_cache(topology_json, dst):
    with open(dst, 'w') as cached_file:
        cached_file.write(json.dumps(topology_json, indent=4, sort_keys=True))

def leer_cache(filename):
    if not os.path.exists(filename):
        return {}
    if not os.path.isfile(filename):
        return {}
    cached_topology = {}
    with open(filename, 'r') as file:
        try:
            cached_topology = json.loads(file.read())
        except:
            return {}
    return cached_topology

def generar_topologia_diferencias(cached, current):
    
    diff_nodes = {'added': [], 'deleted': []}
    diff_links = {'added': [], 'deleted': []}
    diff_merged_topology = {'nodes': [], 'links': []}
    # Parse links from topology dicts into the following format:
    # (topology_link_obj, (source_hostnme, source_port), (dest_hostname, dest_port))
    cached_links = [(x, ((x['srcDevice'], x['srcIfName']), (x['tgtDevice'], x['tgtIfName']))) for x in cached['links']]
    links = [(x, ((x['srcDevice'], x['srcIfName']), (x['tgtDevice'], x['tgtIfName']))) for x in current['links']]
    # Parse nodes from topology dicts into the following format:
    # (topology_node_obj, (hostname,))
    # Some additional values might be added for comparison later on to the tuple above.
    cached_nodes = [(x, (x['IP'],)) for x in cached['nodes']]
    nodes = [(x, (x['IP'],)) for x in current['nodes']]
        
    node_id = 0
    host_id_map = {}
    for raw_data, node in nodes:
        if node in [x[1] for x in cached_nodes]:
            raw_data['id'] = node_id
            host_id_map[raw_data['IP']] = node_id
            raw_data['is_new'] = 'no'
            raw_data['is_dead'] = 'no'
            diff_merged_topology['nodes'].append(raw_data)
            node_id += 1
            continue
    
        diff_nodes['added'].append(node)
        raw_data['id'] = node_id
        host_id_map[raw_data['IP']] = node_id
        raw_data['is_new'] = 'yes'
        raw_data['is_dead'] = 'no'
        diff_merged_topology['nodes'].append(raw_data)
        node_id += 1
    for raw_data, cached_node in cached_nodes:
        if cached_node in [x[1] for x in nodes]:
            continue
        diff_nodes['deleted'].append(cached_node)
        raw_data['id'] = node_id
        host_id_map[raw_data['IP']] = node_id
        raw_data['is_new'] = 'no'
        raw_data['is_dead'] = 'yes'
        raw_data['icon'] = 'dead_node'
        diff_merged_topology['nodes'].append(raw_data)
        node_id += 1
    
    link_id = 0
    for raw_data, link in links:
        src, dst = link
        
        if not (src, dst) in [x[1] for x in cached_links] and not (dst, src) in [x[1] for x in cached_links]:
            diff_links['added'].append((src, dst))
            raw_data['id'] = link_id
            link_id += 1
            raw_data['source'] = host_id_map[src[0]]
            raw_data['target'] = host_id_map[dst[0]]
            raw_data['is_new'] = 'yes'
            raw_data['is_dead'] = 'no'
            diff_merged_topology['links'].append(raw_data)
            continue
        raw_data['id'] = link_id
        link_id += 1
        raw_data['source'] = host_id_map[src[0]]
        raw_data['target'] = host_id_map[dst[0]]
        raw_data['is_new'] = 'no'
        raw_data['is_dead'] = 'no'
        diff_merged_topology['links'].append(raw_data)

    for raw_data, link in cached_links:
        src, dst = link
        if not (src, dst) in [x[1] for x in links] and not (dst, src) in [x[1] for x in links]:
            diff_links['deleted'].append((src, dst))
            raw_data['id'] = link_id
            link_id += 1
            raw_data['source'] = host_id_map[src[0]]
            raw_data['target'] = host_id_map[dst[0]]
            raw_data['is_new'] = 'no'
            raw_data['is_dead'] = 'yes'
            diff_merged_topology['links'].append(raw_data)
            
    return diff_nodes, diff_links, diff_merged_topology

def imprimir_diferencias(diff_result):
    """
    Formatted get_topology_diff result
    console print function.
    """
    diff_nodes, diff_links, *ignore = diff_result
    if not (diff_nodes['added'] or diff_nodes['deleted'] or diff_links['added'] or diff_links['deleted']):
        print('No topology changes since last run.')
        return
    print('Topology changes have been discovered:')
    if diff_nodes['added']:
        print('')
        print('^^^^^^^^^^^^^^^^^^^^')
        print('New Network Devices:')
        print('vvvvvvvvvvvvvvvvvvvv')
        for node in diff_nodes['added']:
            print(f'Hostname: {node[0]}')
    if diff_nodes['deleted']:
        print('')
        print('^^^^^^^^^^^^^^^^^^^^^^^^')
        print('Deleted Network Devices:')
        print('vvvvvvvvvvvvvvvvvvvvvvvv')
        for node in diff_nodes['deleted']:
            print(f'Hostname: {node[0]}')
    if diff_links['added']:
        print('')
        print('^^^^^^^^^^^^^^^^^^^^^^')
        print('New Interconnections:')
        print('vvvvvvvvvvvvvvvvvvvvvv')
        for src, dst in diff_links['added']:
            print(f'From {src[0]}({src[1]}) To {dst[0]}({dst[1]})')
    if diff_links['deleted']:
        print('')
        print('^^^^^^^^^^^^^^^^^^^^^^^^^')
        print('Deleted Interconnections:')
        print('vvvvvvvvvvvvvvvvvvvvvvvvv')
        for src, dst in diff_links['deleted']:
            print(f'From {src[0]}({src[1]}) To {dst[0]}({dst[1]})')
    print('')

