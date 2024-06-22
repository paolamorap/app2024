from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

server_ip="10.0.1.5"
print ("\nFetching stats for...", server_ip)
errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
    cmdgen.CommunityData('public'),
    cmdgen.UdpTransportTarget((server_ip, 161)),
    0,25,
    
    #'1.3.6.1.2.1.17.1.1',
    #"1.3.6.1.2.1.1.3"
    #'1.3.6.1.2.1.17.2.4'
    '1.3.6.1.2.1.2.2.1.10'
    #'1.3.6.1.2.1.17.4.3.1.1'
)
print("Variables de Prueba")
print(errorIndication,errorStatus,errorIndex)
c=0
print(varBindTable)
print("Variables de prueba")

if errorIndication != None:
    print("SI FUNCIONA")
    
for varBindTableRow in varBindTable:
    for name, val in varBindTableRow:
        c+=1
        print(name)
        print(val)