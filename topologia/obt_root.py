import random
from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

def obtr(datos,l2):
    """
    Funcion que permite obtener el ID del Bridge Root de una lista de dispositivos especificos

    Parameters:
    datos(dict):    Diccionario con información de los switches de la Red.
    l2(list):       Lista de direcciones IP de los dispositivos que se requiere consultar el Bridge Root

    Returns:
    r(str):     Id del Bridge Root
    f(int):     Bandera de error de consulta SNMP
    fif(dict):  Diccionario con direcciones IP que mantienen un error
    
    """
    f = 0
    fif = {}
    try:
        ip = l2[0]
        comunidad = datos[ip]["snmp"]
        # Realizar la solicitud SNMP para obtener estadísticas
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
            cmdgen.CommunityData(comunidad),
            cmdgen.UdpTransportTarget((ip, 161)),
            0, 2,
            '1.3.6.1.2.1.17.2.5'
        )

        # Procesar los resultados
        if errorIndication:
            print(f"Error: {errorIndication}")
            f = 1
            fif[ip] = "" 
        else:
            for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    ro =  str(val.prettyPrint())[-12:]
                    
        return ro,f,fif
        
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")  

