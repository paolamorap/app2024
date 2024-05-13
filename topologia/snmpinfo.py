from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

server_ip="192.168.20.3"
print ("\nFetching stats for...", server_ip)
errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
    cmdgen.CommunityData('public'),
    cmdgen.UdpTransportTarget((server_ip, 161)),
    0,25,
    #'1.3.6.1.2.1.17.1.1',
    #"1.3.6.1.2.1.1.3"
    #'1.3.6.1.2.1.17.2.4'
    #'1.3.6.1.2.1.17.2.15.1.3'
    '1.3.6.1.2.1.17.2.15.1.8'
    #'1.3.6.1.2.1.17.4.3.1.1'
)

if errorIndication != None:
    print("SI FUNCIONA")
    
for varBindTableRow in varBindTable:
    for name, val in varBindTableRow:
        print(name.prettyPrint(), val.prettyPrint())