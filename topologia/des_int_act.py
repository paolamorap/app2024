from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

def in_act(dir_ip,com_snmp):
    intef = {}
    for n in dir_ip:
        f = 0
        server_ip=n
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
            cmdgen.CommunityData(com_snmp),
            cmdgen.UdpTransportTarget((server_ip, 161)),
            0,25,
            '1.3.6.1.2.1.2.2.1.8','1.3.6.1.2.1.2.2.1.2'
        )
        inte = []
        for varBindTableRow in varBindTable:
            for name,val in varBindTableRow:
                if (val == 1):
                    inte.append((name.prettyPrint()).split('.')[-1])

                if ((str(val) == "Null0") or ("VLAN" in str(val)) or ("Vlan" in str(val)) or (("vlan" in str(val)))):
                    try:
                        inte.remove((name.prettyPrint()).split('.')[-1])
                    except ValueError:
                        pass
        if (len(inte) > 0):
            intef[n] = inte

    return intef


