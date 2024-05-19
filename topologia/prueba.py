from pysnmp.entity.rfc3413.oneliner import cmdgen
import re

cmdGen = cmdgen.CommandGenerator()

def ma_int(direc, datos):
    d2 = {}
    f = 0
    fif = []
    for server_ip in direc:
        if server_ip not in datos:
            f = 1
            fif.append(server_ip)
            continue
        
        comunidad = datos[server_ip]["snmp"]
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
            cmdgen.CommunityData(comunidad),
            cmdgen.UdpTransportTarget((server_ip, 161)),
            0, 25,
            '1.3.6.1.2.1.2.2.1.2'
        )
        c = 1
        d1 = {}
        if errorIndication:
            f = 1
            fif.append(server_ip)
            continue

        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                if "Ethernet" in val.prettyPrint() and not("0/0" in val.prettyPrint()):
                    cadena = val.prettyPrint()
                    if datos[server_ip]["marca"] == "tplink":
                        interface_name = cadena
                    else:
                        interface_name = cadena
                    d1[str(c)] = interface_name
                    c += 1
        d2[str(server_ip)] = d1
    return d2, f, fif

# Ejemplo de uso
direcciones = ["192.168.20.4", "192.168.20.3", "192.168.20.2"]  # IPs de ejemplo
datos = {
    "192.168.20.4": {"snmp": "public", "marca": "cisco"},
    "192.168.20.3": {"snmp": "public", "marca": "cisco"},
    "192.168.20.2": {"snmp": "public", "marca": "cisco"}
}

resultado, error, fallidas = ma_int(direcciones, datos)
print("Resultado:", resultado)
print("Error:", error)
print("IPs fallidas:", fallidas)
