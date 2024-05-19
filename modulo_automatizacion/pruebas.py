from pysnmp.entity.rfc3413.oneliner import cmdgen

# Generador de comandos SNMP
cmdGen = cmdgen.CommandGenerator()

def bri_id(ips, datos):
    resultados = {}
    fallo = 0
    fallos_individuales = {}

    for server_ip in ips:
        comunidad = datos[server_ip]["snmp"]
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
            cmdgen.CommunityData(comunidad),
            cmdgen.UdpTransportTarget((server_ip, 161)),
            0, 25,
            '1.3.6.1.2.1.17.2.5'
        )

        if errorIndication:
            print('Error en:', server_ip, 'Error:', errorIndication)
            fallo = 1
            fallos_individuales[server_ip] = str(errorIndication)
            continue
        
        if errorStatus:
            print('Error en:', server_ip, 'Status:', errorStatus.prettyPrint())
            fallo = 1
            fallos_individuales[server_ip] = errorStatus.prettyPrint()
            continue

        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                print('IP:', server_ip, 'OID:', name.prettyPrint(), 'Value:', val.prettyPrint())
                # Guardar los valores que terminan en ".1"
                if (name.prettyPrint()).split('.')[-1] == "1":
                    resultados[server_ip] = val.prettyPrint()[2::]

    return resultados, fallo, fallos_individuales

# Lista de IPs de dispositivos y sus datos de comunidad SNMP
ips = ['192.168.20.2', '192.168.20.3']
datos = {
    '192.168.20.2': {'snmp': 'public'},
    '192.168.20.3': {'snmp': 'public'}
}

# Llamar a la función y mostrar los resultados
resultados, fallo, fallos_individuales = bri_id(ips, datos)
print("Resultados finales:", resultados)
print("Fallo general:", fallo)
print("Fallos por IP:", fallos_individuales)

