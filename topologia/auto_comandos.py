import yaml
from netmiko import ConnectHandler
import paramiko
import time
import auto_tplink_comandos


#######################################################################
#------------------------#CONEXION NETMIKO#----------------------------
#######################################################################
def establecer_conexion(device_info):
    try:
        connection = ConnectHandler(**device_info)
        return connection
    except Exception as e:
        print(f"Error conectando a {device_info['ip']}: {e}")
        return None
#######################################################################
#------------------------#CONEXION PARAMIKO#---------------------------
#######################################################################
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
#########################################################################
#------------------------#COMANDOS CISCO#--------------------------------
#########################################################################
#<-----------------------SNMP CONFIGURACION----------------------------->
def configurar_snmp_cisco(connection, community_name):
    commands = [
        f"snmp-server community {community_name} RO",
    ]
    connection.send_config_set(commands)
#<------------------------STP CONFIGURACION----------------------------->

#########################################################################
#------------------------#COMANDOS HPA5120#------------------------------
#########################################################################
#<----------------------SNMP CONFIGURACION------------------------------>
def configurar_snmp_hp(connection, community_name):
    commands = [
        f"snmp-agent community read {community_name}",
    ]
    connection.send_config_set(commands)
#<----------------------STP CONFIGURACION------------------------------->

#########################################################################
#----------------------------#COMANDOS 3COM#-----------------------------
#########################################################################
#-----------------------SNMP CONFIGURCION------------------------------->
def configurar_snmp_3com(ip, username, password, community_name):
    """
    Función para configurar SNMP en un dispositivo 3Com utilizando Paramiko.
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
        send_command(channel, "system-view", wait_time=2)
        send_command(channel, f"snmp-agent community read {community_name}", wait_time=2)
        ssh.close()
        print("Configuración de SNMP completada con éxito.")
    except Exception as e:
        print(f"Error al configurar SNMP en {ip}: {e}")
        ssh.close()
#----------------------------STP CONFIGURACION------------------------------>