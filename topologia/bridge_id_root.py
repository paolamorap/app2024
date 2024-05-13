from pysnmp.entity.rfc3413.oneliner import cmdgen
from collections import Counter
cmdGen = cmdgen.CommandGenerator()

def get_bridge_id_root(ip,comunidad):
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

def obtener_bridge_id_root_switch(ips,datos):
    bridge_root_ip = {}
    for server_ip in ips:
        comunidad = datos[server_ip]["snmp"]
        bridge_id = get_bridge_id_root(server_ip, comunidad)
        if bridge_id:
            bridge_root_ip[str(server_ip)] = bridge_id
    return bridge_root_ip

def obtener_bridge_id_root(ip_values):
    contador = Counter(ip_values.values())
    # Encontrar el bridge ID root 
    bridge_id_root, _ = contador.most_common(1)[0]
    return bridge_id_root

def encontrar_ip_por_bridge_id(diccionario_bridge_id, bridge_id_buscado):
    # Quitamos el prefijo '0x0000' si está presente, ya que no se encuentra en los valores del diccionario
    bridge_id_buscado = bridge_id_buscado.lower().replace('0x0000', '')
    # Buscar en el diccionario
    for ip, bridge_id in diccionario_bridge_id.items():
        if bridge_id.lower() == bridge_id_buscado:
            return ip
    return "No se encontró la IP correspondiente."