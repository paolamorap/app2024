from netmiko import ConnectHandler
import obt_infyam
import os
import paramiko
import time
from pysnmp.entity.rfc3413.oneliner import cmdgen
import leer_cpu
import re
import teleg
import wrinfluxcpu

cmdGen = cmdgen.CommandGenerator()

def send_command(channel, command, wait_time=2, max_buffer=65535):
    """
    Envía un comando a través del canal y devuelve la respuesta.
    """
    channel.send(command + "\n")
    time.sleep(wait_time)  # Espera para asegurar que el comando se haya completado
    # Verifica si el canal está listo para recibir datos
    while not channel.recv_ready(): 
        time.sleep(0.5)
    response = channel.recv(max_buffer).decode('utf-8')
    return response

def interactive_send_command(channel, command, confirmation_text, response, wait_time=2):
    """
    Maneja interacciones que requieren una respuesta interactiva, como confirmaciones.
    """
    # Envía el comando inicial
    channel.send(command + "\n")
    time.sleep(wait_time)
    # Lee la respuesta inicial
    intermediate_response = channel.recv(9999).decode('utf-8')
    # Si se detecta la solicitud de confirmación, envía la respuesta especificada
    if confirmation_text in intermediate_response:
        channel.send(response + "\n")
        time.sleep(wait_time)

    return channel.recv(9999).decode('utf-8')


def comcpu(ip, username, password):
    """
    Función para leer datos de CPU de un switch 3Comm.

    Parameters
    ip(str):           Dirección IP
    username(str):     Nombre de Usuario SSH
    password(str):     Nombre de Usuario SSH

    Return
    v(int):            Valor de Consumo de CPU
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password)  
        # Obtener un canal interactivo
        channel = ssh.invoke_shell()
        # Primero, intentamos entrar en el modo de línea de comandos
        send_command(channel, "_cmdline-mode on", wait_time=2)
        # Esperamos la solicitud de confirmación y enviamos 'Y' para continuar.
        interactive_send_command(
            channel,
            "Y",  # Confirmamos la pregunta para entrar en el modo de línea de comandos.
            "Please input password:",  # La cadena que esperamos antes de enviar la contraseña.
            "512900",  # La contraseña para el modo de línea de comandos.
            wait_time=2  # Tiempo de espera ajustado correctamente.
        )
        # Después de haber entrado en el modo de línea de comandos, continúa con la configuración de SNMP.
        texto = str(send_command(channel, "display cpu-usage", wait_time=2))
        # Expresión regular para encontrar el valor numérico
        patron = r'\d+% in last 5 minutes'

        # Buscar el valor numérico
        resultado = re.search(patron, texto)

        # Extraer el valor numérico
        if resultado:
            valor = resultado.group(0).split()[0]
            v = valor.rstrip('%')
            ssh.close()
            return v
        else:
            print("No se encontró información para los últimos 5 minutos.")

    except Exception as e:
        print(f"Error {ip}: {e}")
        ssh.close()
#----------------------------STP CONFIGURACION------------------------------>

def mon_cpu(info,datos):
    """
    Funcion para Obtener consumo de CPU de los ultimos 5min

    Parameters:
    datos(dict):    Diccionario con información de los dispositivos
    
    Return:
    sal(dict):      Diccionario con el consumo de cpu por dispositivo
    """
    sal = {}
    direc = datos.keys()
    for server_ip in direc:
        print ("\nFetching stats for...", server_ip)
        match datos[server_ip]:
            case "switchs_tplink":
                oid ="1.3.6.1.4.1.11863.6.4.1.1.1.1.2"
            case "switchs_hpV5120":
                oid = "1.3.6.1.4.1.25506.2.6.1.1.1.1.6"
            case "switchs_hpV1910":
                oid = "1.3.6.1.4.1.25506.2.6.1.1.1.1.6"
            case "switchs_3comm":
                sal[server_ip] = comcpu(server_ip,"networking","Ygvfe34a.2018")
                continue
            case "switchs_cisco":
                
                oid = '1.3.6.1.4.1.9.2.1.58'
            case _:
                oid = '1.3.6.1.4.1.9.2.1.58'
        
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
            cmdgen.CommunityData(info[server_ip]["snmp"]),
            cmdgen.UdpTransportTarget((server_ip, 161)),
            0,25,
            oid
        )
        c=0
        for varBindTableRow in varBindTable:
            for name, val in varBindTableRow:
                try:
                    if datos[server_ip] == "switchs_hpV5120" or datos[server_ip] == "switchs_hpV1910":
                        if float(val.prettyPrint())>0:
                            sal[server_ip] = val.prettyPrint()
                            print(val.prettyPrint())
                    else:
                        sal[server_ip] = val.prettyPrint()
                        print(val.prettyPrint())
                except TypeError:
                    pass
    return sal
# Crear el diccionario

current_dir = os.path.dirname(__file__)
nombreyaml = os.path.join(current_dir, 'inventarios', 'dispositivos.yaml')
diccionario_resultante = leer_cpu.crear_diccionario_host_marca(nombreyaml)
datos = obt_infyam.infyam(nombreyaml)
print(diccionario_resultante)
while True:
    salcpu = mon_cpu(datos,diccionario_resultante)
    wrinfluxcpu.wr_influx(salcpu)
    time.sleep(30)