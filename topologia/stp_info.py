from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()
a = {}
f=0

def stp_inf(direc,datos):
    f=0
    fif = {}
    for server_ip in direc:       
        comunidad = datos[server_ip]["snmp"]
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
            cmdgen.CommunityData(comunidad),
            cmdgen.UdpTransportTarget((server_ip, 161)),
            0,25,
            '1.3.6.1.2.1.17.2.15.1.8'
        )
        if errorIndication !=None:
            f = 1
            fif[server_ip] = ""

        errorIndication1, errorStatus1, errorIndex1, varBindTable1 = cmdGen.bulkCmd(
            cmdgen.CommunityData(comunidad),
            cmdgen.UdpTransportTarget((server_ip, 161)),
            0,25,
            '1.3.6.1.2.1.17.2.15.1.9'
        )
        db = []
        pd = []
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                db.append((val.prettyPrint())[-12:])
        for varBindTableRow1 in varBindTable1:
            for name1, val1 in varBindTableRow1:
                pd.append((str(name1).split(".")[-1], (val1.prettyPrint())[-12:]))
        a[server_ip] = [db,pd]
        if errorIndication1 !=None:
            f = 1
            fif[server_ip] = ""

    return a,f,fif

