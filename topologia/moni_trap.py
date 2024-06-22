import ping3
from pysnmp.entity.rfc3413.oneliner import cmdgen
import time
cmdGen = cmdgen.CommandGenerator()
import topologia.mainepops as mainepops
import teleg
import json

direc = ["10.0.1.1","10.0.1.2","10.0.1.3","10.0.1.4","10.0.1.5","10.0.1.6"]
comunidad = "public"

def verificar_hosts(direcciones_ips):
    """
    Verifica si los hosts en la lista de direcciones IP están activos.
    Elimina de la lista los hosts inactivos y devuelve la lista actualizada.
    """
    f = 0
    hosts_activos = []
    for ip in direcciones_ips:
        respuesta = ping3.ping(ip, timeout=3)  # Timeout de 1 segundo
        if respuesta is not None:
            hosts_activos.append(ip)
        else:
            print(f"{ip} está inactivo.")

    return hosts_activos,f

def mon_stp(direc):
    a = []
    for server_ip in direc:
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
            cmdgen.CommunityData(comunidad),
            cmdgen.UdpTransportTarget((server_ip, 161)),
            0,25,
            '1.3.6.1.2.1.17.2.4'
        )
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                #if int(val) <= -1:
                #  print("La Topologia Cambio")
                a.append(str(val))
    return a


ep1 = []
ep2 = []
ep3 = []
la = []
# Nombre del archivo
conexlis = 'conex.txt'

# Guardar la lista en el archivo en formato JSON
with open(conexlis, 'w') as archivo:
    json.dump(la, archivo)


teleg.enviar_mensaje("INICIANDO SISTEMA \n")


while True:
    with open(conexlis, 'r') as archivo:
        la = json.load(archivo)

    f1 = 1

    """
    2 Etapas de Monitoreo
    Verificar que los switch esten activos
    Monitorear cambios en Interfaces
    Monitorear cambios en STP
    """
    #Etapa 1
    ea3,f = verificar_hosts(direc)
    ea1 = mon_stp(list(ea3))


    print("Monitoreando")
    if ea3 != ep3:
        f = 1
        f1 = 0
        if len(ea3) < len(ep3):
            conjunto1 = {tuple(sorted(tup)) for tup in ea3}
            conjunto2 = {tuple(sorted(tup)) for tup in ep3}

            # Eliminar los elementos de la tupla2 que coinciden con la tupla1
            tupla2_filtrada = [tup for tup in ep3 if tuple(sorted(tup)) not in conjunto1]
            for tupa in tupla2_filtrada:
                teleg.enviar_mensaje("Dispositivo sin acceso: "+str(tupa)+"\n")

        if len(ea3) > len(ep3):
            conjunto1 = {tuple(sorted(tup)) for tup in ep3}
            conjunto2 = {tuple(sorted(tup)) for tup in ea3}

            # Eliminar los elementos de la tupla2 que coinciden con la tupla1
            tupla2_filtrada = [tup for tup in ea3 if tuple(sorted(tup)) not in conjunto1]
            for tupa in tupla2_filtrada:
                teleg.enviar_mensaje("Dispositivo nuevamente con acceso: "+str(tupa)+"\n")
    ep3=ea3

    if ea1 != ep1 and f1 == 1:
        f = 1
        time.sleep(10)
    ep1=ea1

    if f == 1:
        print(la)
        ln = mainepops.maintop(list(ea3))
        print(ln)
        if la == ln:
            print("Actualizacion de Roles de Puertos - STP")

        if len(la) == len(ln):
           conjunto1 = {tuple(sorted(tup)) for tup in la}
           conjunto2 = {tuple(sorted(tup)) for tup in ln}

           # Eliminar los elementos de la tupla2 que coinciden con la tupla1
           tupla2_filtrada = [tup for tup in ln if tuple(sorted(tup)) not in conjunto1]
           if len(tupla2_filtrada) > 0:
              for tupa in tupla2_filtrada:
                a = "Se levantó la conexión entre los equipos\n"+tupa[0].split("-")[0]+"\n"+tupa[1].split("-")[0]+"\n"
                teleg.enviar_mensaje(a)

           conjunto1 = {tuple(sorted(tup)) for tup in ln}
           conjunto2 = {tuple(sorted(tup)) for tup in la}

           # Eliminar los elementos de la tupla2 que coinciden con la tupla1
           tupla2_filtrada = [tup for tup in la if tuple(sorted(tup)) not in conjunto1]
           if len(tupla2_filtrada) > 0:
              for tupa in tupla2_filtrada:
                 a = "Se perdio la conexión entre los equipos\n"+tupa[0].split("-")[0]+"\n"+tupa[1].split("-")[0]+"\n"
                 teleg.enviar_mensaje(a)


        if len(la) < len(ln):
            conjunto1 = {tuple(sorted(tup)) for tup in la}
            conjunto2 = {tuple(sorted(tup)) for tup in ln}

            # Eliminar los elementos de la tupla2 que coinciden con la tupla1
            tupla2_filtrada = [tup for tup in ln if tuple(sorted(tup)) not in conjunto1]
            for tupa in tupla2_filtrada:
                a = "Se levantó la conexión entre los equipos\n"+tupa[0].split("-")[0]+"\n"+tupa[1].split("-")[0]+"\n"
                teleg.enviar_mensaje(a)

        if len(ln) < len(la):
            # Convertir las tuplas en conjuntos después de ordenar los elementos
            conjunto1 = {tuple(sorted(tup)) for tup in ln}
            conjunto2 = {tuple(sorted(tup)) for tup in la}

            # Eliminar los elementos de la tupla2 que coinciden con la tupla1
            tupla2_filtrada = [tup for tup in la if tuple(sorted(tup)) not in conjunto1]

            for tupa in tupla2_filtrada:
                a = "Se perdió la conexión entre los equipos\n"+tupa[0].split("-")[0]+"\n"+tupa[1].split("-")[0]+"\n"
                teleg.enviar_mensaje(a)
   
    with open(conexlis, 'w') as archivo:
        json.dump(ln, archivo)


    time.sleep(10)  # Pausa la ejecución durante 1 segundo