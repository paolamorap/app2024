import ping3
from pysnmp.entity.rfc3413.oneliner import cmdgen
import time
cmdGen = cmdgen.CommandGenerator()
import mainepops
import teleg
import json
import con_red
import wrinflux
import dtsnmp
import readuptime

direc = ["10.0.1.1","10.0.1.2","10.0.1.3","10.0.1.4","10.0.1.5"]
comunidad = "public"

def verificar_hosts(direcciones_ips):
    """
    Verifica si los hosts en la lista de direcciones IP están activos.
    Elimina de la lista los hosts inactivos y devuelve la lista actualizada.
    """
    f = 0
    hosts_activos = []
    hosts_inactivos = []
    for ip in direcciones_ips:
        respuesta = ping3.ping(ip, timeout=3)  # Timeout de 1 segundo
        if respuesta is not None:
            hosts_activos.append(ip)
        else:
            print(f"{ip} está inactivo.")
            hosts_inactivos.append(ip)
            f=1
    return hosts_activos,hosts_inactivos,f

def mon_int(direc):
    l_int = []
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
        else:
           l_int = list(map(lambda x: ((x[0][1]).prettyPrint()),varBindTable))

    return l_int,f,fif

# Lista de direcciones IP para verificar
#Contadores de Control
ci = 0
c = 0

#Listas con estados de interfaces y de dispositivos
epint = []
epping = []

cp = [] #COnexiones Pasadas

#Listas de enlaces redundantes
enr = []
enr1 = []

# Crear un diccionario con claves de la lista y valores iniciales 0
dinac = {clave: 0 for clave in direc}
diint = {clave: 0 for clave in direc}
diest = {clave: 1 for clave in direc}
disnmp = {clave: 0 for clave in direc}
dicpu = {clave: 0 for clave in direc}


teleg.enviar_mensaje("INICIANDO SISTEMA \n")
while True:
    fsnmp = 0
    fsi = 0
    fping = 0 
    diesnmp = []
    faux = 0
    fp = 0
    infuptime = {} #Diccionario con Tiempos de Actividad
    print("Monitoreando")

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%--Monitoreo por Ping--%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
       eaping: estado actual - Lista de con dispositivos con ping exitoso
       epping: estado pasado - Lista de con dispositivos con ping exitoso
    """
    print("")
    print(" -------------ep,ea Control de monitoreo por PINGS ----------")
    print(epping)
    eaping,inactivos,fping = verificar_hosts(direc)
    #print(diest)
    #Perdido de Conexion Mayor a 10seg
    if fping == 1:
    #Proceso para contar interrumpciones rapidas
       for i in inactivos:
           if diest[i] == 0:
                dinac[i] += 1
                diint[i] += 1
    #---------------------------------------
       print("Se bajo conexión")
       time.sleep(5)
       eaping,inactivos,fp = verificar_hosts(direc)


    #Proceso para contar interrumpciones rapidas
    for x in direc:
        if dinac[x] >= 4:
            teleg.enviar_mensaje("Se ha tenido Varias interrumpciones con el dispositivo: "+x)
            dinac[x] = 0

    #---------------------------------------

    #print(dinac)
    if ci == 10:
        dinac = {clave: 0 for clave in direc}
        ci = 0

    print(eaping)
    print("------------------------------------------------------------------------------------")
    print("")

    if eaping != epping:
        print("Se comparo lista de pings - Listas Diferentes")
        fp = 1
        faux = 1
        # Convertir las listas a conjuntos
        epping_set = set(epping)
        eaping_set = set(eaping)
        # Encontrar los elementos diferentes
        diferentes_en_epping = epping_set - eaping_set
        diferentes_en_eaping = eaping_set - epping_set
        for elemento in diferentes_en_epping:
            teleg.enviar_mensaje("Dispositivo sin acceso: "+str(elemento)+"\n")
            diest[str(elemento)] = 1
        for elemento in diferentes_en_eaping:
            teleg.enviar_mensaje("Dispositivo nuevamente con acceso: "+str(elemento)+"\n")
            diest[str(elemento)] = 0
            
    epping=eaping


    #%%%%Seccion para monitoreo de Reinicio del Equipo%%%%%%%%%%%%%%%%%%%%
    infuptime = readuptime.con_uptime(list(eaping))
    for i in infuptime.keys():
        if (infuptime[i] <= 35000) and (dicpu[i] == 0) :
            teleg.enviar_mensaje("EL dispositivo" + str(i) + " se reinicio")
            dicpu[i] = 1
        elif (infuptime[i] >= 35000):
            dicpu[i] = 0
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%--Monitoreo de Interfaces---%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
        eaint: estado actual: Lista con estado de las interfaces de los dispositivos
        epint: estado pasado: Lista con estado de las interfaces de los dispositivos
    """

    if c == 5 :
        ci += 1
        c = 0
        if faux == 0:
        # print(epint)
            eaint,fsi,diesnmp = mon_int(list(eaping))
        # print(eaint)
        if eaint != epint:
            print("Se comparo lista de interfaces - Listas Diferentes")
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
        time.sleep(3)
        dfsnmp =[]
        print("Se ejecuto el descubrimiento de Interfaces")
        #print(enr)
        #print(enr1)
        #print(cp)
        ca,fsnmp,dfsnmp1 = mainepops.main_top(list(eaping))
        dfsnmp = dtsnmp.snmt(dfsnmp1,diesnmp)
        #print(ca)
        #print("DIccionario SNMP")
        print("")
        print("-------------------disnp,fsnmp,fsi----Control de error de snmp-----------------------")
        print(disnmp,fsnmp,fsi)
        print("------------------------------------------------------------------------------------")
        print("")
        #print("-"*20)
        #Control de fallas de conexiones con SNMP
        if fsnmp == 1 or fsi == 1:
            for i in dfsnmp :
                if disnmp[i] == 0:
                    dinac[i] += 1
                    diint[i] += 1
                    disnmp[i] = 1
                    teleg.enviar_mensaje("Error de la conexion snmp: " + str(i))
        else:
            disnmp = {clave: 0 for clave in direc}
        #-----------------------------
        if cp == ca:
            print("No se modifico las conexiones")

        if len(cp) == len(ca):
           conjunto1 = {tuple(sorted(tup)) for tup in cp}
           conjunto2 = {tuple(sorted(tup)) for tup in ca}
           # Eliminar los elementos de la tupla2 que coinciden con la tupla1
           tupla2_filtrada = [tup for tup in ca if tuple(sorted(tup)) not in conjunto1]
           if len(tupla2_filtrada) > 0:
              for tupa in tupla2_filtrada:
                a = "Se levantó la conexión entre los equipos\n"+tupa[0].split("-")[0]+"\n"+tupa[1].split("-")[0]+"\n"
                teleg.enviar_mensaje(a)

           conjunto1 = {tuple(sorted(tup)) for tup in ca}
           conjunto2 = {tuple(sorted(tup)) for tup in cp}

           # Eliminar los elementos de la tupla2 que coinciden con la tupla1
           tupla2_filtrada = [tup for tup in cp if tuple(sorted(tup)) not in conjunto1]
           if len(tupla2_filtrada) > 0:
              for tupa in tupla2_filtrada:
                 a = "Se perdio la conexión entre los equipos\n"+tupa[0].split("-")[0]+"\n"+tupa[1].split("-")[0]+"\n"
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
                    a = "Se levantó una conexión redundante entre los equipos\n"+tupa[0].split("-")[0]+"\n"+tupa[1].split("-")[0]+"\n"
                else:
                    a = "Se levantó la conexión entre los equipos\n"+tupa[0].split("-")[0]+"\n"+tupa[1].split("-")[0]+"\n"
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
                    a = "Se perdió una conexión redundante entre los equipos\n"+tupa[0].split("-")[0]+"\n"+tupa[1].split("-")[0]+"\n"
                else:
                    a = "Se perdió la conexión entre los equipos\n"+tupa[0].split("-")[0]+"\n"+tupa[1].split("-")[0]+"\n"
                teleg.enviar_mensaje(a)
        #Identificacion de enlaces redundantes
        enr,enr1 = con_red.id_red(ca)
    #-----------------------------------------Fin de Descubrimiento de topologia--------------------------------------------------------

    cp = ca
    c+=1
    wrinflux.wr_influx(diint)
    time.sleep(1)  # Pausa la ejecución durante 1 segundo