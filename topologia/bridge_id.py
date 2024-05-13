from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()


def bri_id(ips,datos):
    a = {}
    f = 0
    fif = {}

    for server_ip in ips:
        comunidad = datos[server_ip]["snmp"]
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
            cmdgen.CommunityData(comunidad),
            cmdgen.UdpTransportTarget((server_ip, 161)),
            0,25,
            '1.3.6.1.2.1.2.2.1.6'
        )
        if errorIndication != None:
            f = 1
            fif[server_ip] = ""
        
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                if  (name.prettyPrint()).split('.')[-1] == "1":
                    a[server_ip] = val.prettyPrint()[2::]
    return a,f,fif