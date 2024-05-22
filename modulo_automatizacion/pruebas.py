from pysnmp.hlapi import getCmd, CommunityData, UdpTransportTarget, SnmpEngine, ContextData, ObjectType, ObjectIdentity
import re

def obtener_informacion_dispositivos(ips, datos):
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

# Lista de IPs y datos SNMP (comunidades) de los dispositivos
ips = ['192.168.20.2', '192.168.20.3']
datos = {
    '192.168.20.2': {'snmp': 'public'},
    '192.168.20.3': {'snmp': 'public'}
}

# Llamada a la función y mostrar resultados
resultados = obtener_informacion_dispositivos(ips, datos)
print(resultados)
