from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()
def stp_status(direc,stpi,datos):
    """
    Permite obtener los puertos bloqueados por el protocolo STP de un switch 
    
    Parameters:
    direc(list):    Direcciones IP de los dispositivos que se requiere conocer la información    
    stpi(dict):     Interfaces de los switches
    datos(dict):    Datos con información de los switches de la Red
    
    Return:
    sl(list):   Lista con la Dirección IP y el puerto bloqueado del dispositivo
    f(int):     Bandera para detectar errores en consulta SNMP
    fif(list):  Direcciones IP que tuvieron fallas en la consulta
    """
    
    sl = []
    f=0
    fif=[]
    for server_ip in direc:
        comunidad = datos[server_ip]["snmp"]
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
            cmdgen.CommunityData(comunidad),
            cmdgen.UdpTransportTarget((server_ip, 161)),
            0,25,
            '1.3.6.1.2.1.17.2.15.1.3'
        )
        if errorIndication != None:
           f = 1
           fif.append(server_ip)
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                if server_ip in stpi.keys():
                    p = str(name).split(".")[-1]
                    lp = stpi[server_ip]
                    if p in lp:
                        if val.prettyPrint() == "2":
                            sl.append(server_ip +"-"+p)
    return sl,f,fif