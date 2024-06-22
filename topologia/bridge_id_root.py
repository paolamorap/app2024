from pysnmp.entity.rfc3413.oneliner import cmdgen
from collections import Counter
cmdGen = cmdgen.CommandGenerator()

def get_bridge_id_root(ip, comunidad):

    """
    Realiza una solicitud SNMP para obtener el Bridge Root ID de un dispositivo específico en la red.
    
    Parámetros:
    - ip (str): Dirección IP del dispositivo objetivo.
    - comunidad (str): Comunidad SNMP para acceder al dispositivo.

    Retorna:
    - str: El Bridge Root ID del dispositivo si la solicitud es exitosa.
    - None: Si ocurre un error durante la solicitud SNMP o si no se encuentra el valor.
    """

    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
        cmdgen.CommunityData(comunidad),
        cmdgen.UdpTransportTarget((str(ip), 161)),
        0, 2,
        '1.3.6.1.2.1.17.2.5'
    )

    # Verificar si hay errores y manejarlos apropiadamente
    if errorIndication:
        print(f"Error: {errorIndication}")
        return None
    elif errorStatus:
        print(f"Error: {errorStatus.prettyPrint()} at {errorIndex}")
        return None

    # Procesar los resultados y extraer el valor del Bridge ID Root
    for varBindTableRow in varBindTable:
        for name, val in varBindTableRow:
            if val.prettyPrint() != 'No more variables left in this MIB View':
                return val.prettyPrint()
    return None


def obtener_bridge_id_root_switch(ips, datos):
    """
    Obtiene el Bridge Root ID para múltiples dispositivos basado en sus direcciones IP y datos SNMP.

    Parámetros:
    - ips (list): Lista de direcciones IP de los dispositivos.
    - datos (dict): Diccionario con datos de los dispositivos donde se incluye la comunidad SNMP. 

    Retorna:
    - dict: Diccionario con IPs de dispositivos como claves y sus Bridge Root IDs como valores.

    Itera sobre una lista de direcciones IP, obtiene la comunidad SNMP de cada uno, y usa `get_bridge_id_root`
    para obtener el Bridge Root ID. Los resultados se almacenan en un diccionario que se retorna al final.
    """
    bridge_root_ip = {}
    for server_ip in ips:
        comunidad = datos[server_ip]["snmp"]
        bridge_id = get_bridge_id_root(server_ip, comunidad)
        if bridge_id:
            bridge_root_ip[str(server_ip)] = bridge_id
    return bridge_root_ip


def obtener_bridge_id_root(ip_values):
    """
    Determina el Bridge Root ID más común entre varios dispositivos.

    Parámetros:
    - ip_values (dict): Diccionario con valores de Bridge ID como valores.

    Retorna:
    - str: El Bridge ID más común entre los valores proporcionados.

    Utiliza la clase `Counter` para contar la frecuencia de cada Bridge ID y retorna el más común.
    """
    contador = Counter(ip_values.values())
    bridge_id_root, _  = contador.most_common(1)[0]

    return bridge_id_root


def encontrar_ip_por_bridge_id(ip_values, diccionario_bridge_id):
    """
    Busca una dirección IP basada en el Bridge ID especificado.

    Parámetros:
    - diccionario_bridge_id (dict): Diccionario con IPs como claves y Bridge IDs como valores.
    - bridge_id_buscado (str): Bridge ID que se busca en el diccionario.

    Retorna:
    - str: La dirección IP correspondiente al Bridge ID buscado.
    - "No se encontró la IP correspondiente.": Si el Bridge ID no se encuentra en el diccionario.

    Elimina los primeros 6 caracteres del `bridge_id_buscado` y luego busca en el diccionario para encontrar
    la IP correspondiente. Si no encuentra una coincidencia, retorna un mensaje indicando que no se encontró la IP.
    """
    # Eliminar los primeros 6 caracteres del bridge_id_buscado
    bridge_id_buscado = obtener_bridge_id_root(ip_values)
    bridge_id_buscado = bridge_id_buscado[6:].lower()
    
    # Buscar en el diccionario
    for ip, bridge_id in diccionario_bridge_id.items():
        if bridge_id.lower() == bridge_id_buscado:
            return ip
    return "No se encontró la IP correspondiente."