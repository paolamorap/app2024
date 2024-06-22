import con_red
import wrinflux
import ping3
from pysnmp.entity.rfc3413.oneliner import cmdgen
import time
cmdGen = cmdgen.CommandGenerator()
import mainepops
import teleg
import obt_infyam
import dtsnmp
import readuptime
import os 

#Valores de configuración del script
current_dir = os.path.dirname(__file__)
config_file = current_dir+'/configuracion/configuracion_monitoreo.json'
config = obt_infyam.read_config(config_file)
timeping = config.get('montoleranciaping', 5)  
timexec = config.get('montiempoexec', 10) 
timeint = config.get('moninterfaces', 5)  
nombreyaml = os.path.join(current_dir, 'inventarios', 'dispositivos.yaml')
datos = obt_infyam.infyam(nombreyaml)
direc = datos.keys()
print(direc)
comunidad = datos[list(direc)[0]]["snmp"]



def verificar_hosts(direcciones_ips):
    """
    Verifica si los hosts en la lista de direcciones IP están activos.
    Elimina de la lista los hosts inactivos y devuelve la lista actualizada.

    Parameters:
    direcciones_ips(list):      Direcciones IP de los switch a consultar estado

    Return:
    hosts_activos(list):        Direcciones IP de equipos activos
    hosts_inactivos(list):      Direcciones IP de equipos inactivos
    f(int):                     Bandera para detectar que se perdio la conexiòn con algun equipo

    """
    f = 0
    hosts_activos = []
    hosts_inactivos = []

    for ip in direcciones_ips:
        respuesta = ping3.ping(ip, timeout=3)  # Timeout de 1 segundo
        if respuesta is not None:
            hosts_activos.append(ip)
        else:
            print(f"Switch {ip} :está inactivo.")
            hosts_inactivos.append(ip)
            f=1

    return hosts_activos,hosts_inactivos,f

def mon_int(direc):
    """
    Permite consultar el estado de las interfaces de los equipos

    Parameters:
    direc(list):

    Return:
    info_int_disp(list):    Estado de las interfaces de los equipos
    f(int):                 Bandera para detectar probleams en la consulta SNMP
    fif(list):              Dispositivos que tuvieron problemas con la consulta SNMP
    """
    info_int_disp = []
    f = 0
    fif = []
    for server_ip in direc:
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
            cmdgen.CommunityData(comunidad),
            cmdgen.UdpTransportTarget((server_ip, 161)),
            0,25,
            '1.3.6.1.2.1.2.2.1.8'
        )
        if errorIndication != None:
           f = 1
           fif.append(server_ip)
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                #if int(val) <= -1:
                #  print("La Topologia Cambio")
                info_int_disp.append(str(val))
    return info_int_disp,f,fif

# Lista de direcciones IP para verificar
#Contadores de Control
#Control de reincio de interrupciones
ci = 0 

#Control de monitoreo de Interfaces
c = 0

#Listas con estados de interfaces y de dispositivos
epint = []
epping = []

cp = [] #COnexiones Pasadas

#Listas de enlaces redundantes
enr = []
enr1 = []

#Diccionario con estados para control de conteos

diint = {clave: 0 for clave in direc}       #Número de interrupciones sin reinicio
diest = {clave: 1 for clave in direc}       #Detecta si ya se conto un dispositivo inactivo
disnmp = {clave: 0 for clave in direc}      #Detecta si ya se conto un dispositivo con fallo en consulta snmp
diuptime = {clave: 0 for clave in direc}    #Detecta si ya se notifico el reinicio de un dispositivo



teleg.enviar_mensaje("Bienvenido - Iniciando Monitoreo\n")
while True:
    """
    Bucle principal para mantener un monitoreo cada 10 Segundos
    """
    #Banderas para controlar errores 
    fsnmp = 0 #Bandera para detectar falla de consulta SNMP
    fsi = 0   #Bandera para detectar falla de consulta SNMP
    fping = 0 #Bandera de ping de falla rapida
    faux = 0  #Eventos en el monitoreo de pings
    fp = 0    #Bandera para contar fallo de ping con perdida de conexión total
    diesnmp = []    #Guarda el estao de error en consultas snmp
    infuptime = {} #Diccionario con Tiempos de Actividad
    diint = {clave: 0 for clave in direc}    #Bandera para notificar de interrupcion

    print("*"*20+"Monitoreando"+"*"*20)

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%--Monitoreo por Ping--%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
       eaping: estado actual - Lista de con dispositivos con ping exitoso
       epping: estado pasado - Lista de con dispositivos con ping exitoso
    """
    print("")
    print("-"*20+"Dispositivos Activos"+"-"*20)
    #print(epping)
    eaping,inactivos,fping = verificar_hosts(direc)
    #print(diest)
    #Perdido de Conexion Mayor a 5seg

    #*****************Conteo de interrupciones *************
    if fping == 1:
    #Proceso para contar interrumpciones rapidas
       for i in inactivos:
           if diest[i] == 0:
                diint[i] += 1
    #---------------------------------------
       print("Se perdió ping con algun dispositivo")
       time.sleep(timeping) #Se espera 5 segundos para consultar nuevamente el estado del switch
       eaping,inactivos,fp = verificar_hosts(direc)

    #---------------------------------------
    print(eaping)
    print("-"*50)
    print("")

    if eaping != epping:
        print("Se agregaron/eliminaron dispositivos - PING")
        fp = 1
        faux = 1
        # Convertir las listas a conjuntos
        epping_set = set(epping)
        eaping_set = set(eaping)
        # Encontrar los elementos diferentes
        diferentes_en_epping = epping_set - eaping_set
        diferentes_en_eaping = eaping_set - epping_set
        for elemento in diferentes_en_epping:
            teleg.enviar_mensaje("Conexión fallida: "+str(elemento)+"\n")
            diest[str(elemento)] = 1
        for elemento in diferentes_en_eaping:
            teleg.enviar_mensaje("Conexión establecida: "+str(elemento)+"\n")
            diest[str(elemento)] = 0
            
    epping=eaping


    #%%%%Seccion para monitoreo de Reinicio del Equipo%%%%%%%%%%%%%%%%%%%%
    infuptime = readuptime.con_uptime(list(eaping))
    for i in infuptime.keys():
        if (infuptime[i] <= 22000) and (diuptime[i] == 0) :
            teleg.enviar_mensaje("EL dispositivo" + str(i) + " se reinició")
            diuptime[i] = 1
        elif (infuptime[i] >= 22000):
            diuptime[i] = 0
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%--Monitoreo de Interfaces---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
        eaint: estado actual: Lista con estado de las interfaces de los dispositivos
        epint: estado pasado: Lista con estado de las interfaces de los dispositivos
    """

    #*********************Inspección de las interfaces por seguridad*****************
    if c == timeint :
        ci += 1
        c = 0
        if faux == 0: #En caso de no existieron eventos en el monitoreo por ping
        # print(epint)
            print("Consulta estados de Interfaces - SNMP")
            print("")
            eaint,fsi,diesnmp = mon_int(list(eaping))
        # print(eaint)
        if eaint != epint:
            print("Existió cambios en el estado de las interfaces - SNMP")
            print("")
            fp = 1
        epint=eaint
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%--Descubrir Topologia ---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    """
        f: Bandaera para activar descubrimiento
        cp: conexiones pasadas  - Lista de conexiones
        ca: conexiones actuales - Lista de conexiones
    """

    if fp == 1:
        time.sleep(5)
        dfsnmp =[] #Lista con direcciones IP de todos los equipos con problemas en la consulta snmp
        print("Se ejecuto algoritmo de descubrimiento de Topología")
        #print(enr)
        #print(enr1)
        #print(cp)
        ca,fsnmp,dfsnmp1 = mainepops.main_top(list(eaping))
        dfsnmp = dtsnmp.snmt(dfsnmp1,diesnmp)
        print("_"*20+"Conexiones Detectadas"+"_"*20)
        print(ca)
        #print("DIccionario SNMP")
        print("")
        print("-"*20+"Errores en consulta snmp"+"-"*20)
        print(disnmp,fsnmp,fsi)
        print("-"*50)
        print("")
        #print("-"*20)
        #Control de fallas de conexiones con SNMP
        if fsnmp == 1 or fsi == 1:
            for i in dfsnmp :
                if disnmp[i] == 0:
                    diint[i] += 1
                    disnmp[i] = 1 #Bandera de errores en SNMP
                    teleg.enviar_mensaje("Error en la consulta SNMP: " + str(i))
        else:
            #Restablece la bandera de errores SNMP
            disnmp = {clave: 0 for clave in direc}
        #-----------------------------
        if cp == ca:
            print("No se modifico la topología")
        if len(cp) == len(ca):
           conjunto1 = {tuple(sorted(tup)) for tup in cp}
           conjunto2 = {tuple(sorted(tup)) for tup in ca}
           # Eliminar los elementos de la tupla2 que coinciden con la tupla1
           tupla2_filtrada = [tup for tup in ca if tuple(sorted(tup)) not in conjunto1]
           if len(tupla2_filtrada) > 0:
              for tupa in tupla2_filtrada:
                a = "Se levantó la conexión entre los equipos: \n"+tupa[0].split("-")[0]+"\n"+tupa[1].split("-")[0]+"\n"
                teleg.enviar_mensaje(a)

           conjunto1 = {tuple(sorted(tup)) for tup in ca}
           conjunto2 = {tuple(sorted(tup)) for tup in cp}

           # Eliminar los elementos de la tupla2 que coinciden con la tupla1
           tupla2_filtrada = [tup for tup in cp if tuple(sorted(tup)) not in conjunto1]
           if len(tupla2_filtrada) > 0:
              for tupa in tupla2_filtrada:
                 a = "Se perdió la conexión entre los equipos: \n"+tupa[0].split("-")[0]+"\n"+tupa[1].split("-")[0]+"\n"
                 teleg.enviar_mensaje(a)


        if len(cp) < len(ca):
            conjunto1 = {tuple(sorted(tup)) for tup in cp}
            conjunto2 = {tuple(sorted(tup)) for tup in ca}

            # Eliminar los elementos de la tupla2 que coinciden con la tupla1
            tupla2_filtrada = [tup for tup in ca if tuple(sorted(tup)) not in conjunto1]
            for tupa in tupla2_filtrada:
               # print(tupa[0])
               # print(tupa[1])
                if str(sorted(list([tupa[0].split("-")[0],tupa[1].split("-")[0]]))) in enr1:
                    a = "Se ha establecido una conexión redundante entre los equipos: \n"+tupa[0].split("-")[0]+"\n"+tupa[1].split("-")[0]+"\n"
                else:
                    a = "Se levantó la conexión entre los equipos: \n"+tupa[0].split("-")[0]+"\n"+tupa[1].split("-")[0]+"\n"
                teleg.enviar_mensaje(a)

        if len(ca) < len(cp):
            # Convertir las tuplas en conjuntos después de ordenar los elementos
            conjunto1 = {tuple(sorted(tup)) for tup in ca}
            conjunto2 = {tuple(sorted(tup)) for tup in cp}
            # Eliminar los elementos de la tupla2 que coinciden con la tupla1
            tupla2_filtrada = [tup for tup in cp if tuple(sorted(tup)) not in conjunto1]
            for tupa in tupla2_filtrada:
                #print(tupa[0])
                #print(tupa[1])

                if str(sorted(list([tupa[0].split("-")[0],tupa[1].split("-")[0]]))) in enr:
                    a = "Se ha perdido una conexión redundante entre los equipos\n"+tupa[0].split("-")[0]+"\n"+tupa[1].split("-")[0]+"\n"
                else:
                    a = "Se perdió la conexión entre los equipos\n"+tupa[0].split("-")[0]+"\n"+tupa[1].split("-")[0]+"\n"
                teleg.enviar_mensaje(a)
        #Identificacion de enlaces redundantes
        enr,enr1 = con_red.id_red(ca)
    #-----------------------------------------Fin de Descubrimiento de topologia--------------------------------------------------------

    cp = ca
    c+=1
    wrinflux.wr_influx(diint)
    time.sleep(timexec)  # Pausa la ejecución durante 10 segundos