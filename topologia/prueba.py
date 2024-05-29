from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

def probar_oid(ip, comunidad, oid):
    print(f"Consultando {ip} con comunidad {comunidad} para OID {oid}")
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(comunidad),
        cmdgen.UdpTransportTarget((ip, 161)),
        oid
    )

    if errorIndication:
        print(f"Error en {ip} para OID {oid}: {errorIndication}")
    elif errorStatus:
        print(f"Error en {ip} para OID {oid}: {errorStatus.prettyPrint()} at {errorIndex}")
    else:
        for name, val in varBinds:
            print(f"{name.prettyPrint()} = {val.prettyPrint()}")

def main():
    ips = ["192.168.122.3", "192.168.122.4"]
    comunidad = "public"
    oid = '1.3.6.1.2.1.17.2.5'  # Cambia esta OID por la que quieras probar

    for ip in ips:
        probar_oid(ip, comunidad, oid)

if __name__ == "__main__":
    main()
