from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

def stp_inf(direc,datos):
    """
    Funcion para obtener la información de un grupo de switches acerca del protocolo STP 
    Información:
    Bridge ID/ Bridge Designed
    Interfaces Conectadas

    Parameters:
    direc(list):    Direcciones IP de los switches
    datos(dict):    Información de los switches
    
    Return:
    stp_data(dict):     Diccionario con la información STP por dispositivo
    f(int):             Bandera para control de errores en la consulta SNMP
    fif(dict):          Diccionario con los switches que tuvieron problemas en la consulta
    """
    stp_data = {}
    f = 0
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
        stp_data[server_ip] = [db,pd]
        if errorIndication1 !=None:
            f = 1
            fif[server_ip] = ""

    return stp_data,f,list(fif.keys())