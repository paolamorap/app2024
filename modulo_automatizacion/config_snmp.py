import paramiko
import conexion_ssh
from textwrap import dedent

#--------------------------------------------------------------------------------------------
#********************************* Configuracion CISCO **************************************
#--------------------------------------------------------------------------------------------

def configurar_snmp_cisco(connection, community_name, permiso):
    """
    Función para configurar SNMP en dispositivos CISCO utilizando Netmiko.

    Parámetros:
        comunity_name (str): Nombred de la comunidad.
        permiso (srt): Permiso de lectura RO o escritura RW. 
    """
    commands = [
        f"snmp-server community {community_name} {permiso}",
    ]
    connection.send_config_set(commands)

def configurar_snmp_acl_cisco(connection, community_name, permiso, id_acl):
    """
    Función para configurar SNMP en dispositivos CISCO utilizando Netmiko.

    Parámetros:
        comunity_name (str): Nombred de la comunidad.
        permiso (srt): Permiso de lectura RO o escritura RW. 
        id_acl (number): Numero de la lista de acceso.
    """
    commands = [
        f"snmp-server community {community_name} {permiso} {id_acl}",
    ]
    connection.send_config_set(commands)

#--------------------------------------------------------------------------------------------
#****************************** Configuracion HPA5120 ***************************************
#--------------------------------------------------------------------------------------------

def configurar_snmp_hp(connection, community_name, permiso):
    """
    Función para configurar SNMP en dispositivos HPA5120 utilizando Netmiko.

    Parámetros:
        comunity_name (str): Nombred de la comunidad.
        permiso (srt): Permiso de lectura {read} o escritura {write}. 
    """
    commands = [
        f"snmp-agent community {permiso} {community_name}",
    ]
    connection.send_config_set(commands)

def configurar_snmp_acl_hp(connection, community_name, permiso, id_acl):
    """
    Función para configurar SNMP en dispositivos HPA5120 utilizando Netmiko.

    Parámetros:
        comunity_name (str): Nombred de la comunidad.
        permiso (srt): Permiso de lectura {read} o escritura {write}. 
        id_acl (number): Numero de la lista de acceso.
    """
    commands = [
        f"snmp-agent community {permiso} {community_name} acl {id_acl}",
    ]
    connection.send_config_set(commands)



#--------------------------------------------------------------------------------------------
#*******************************Configuracion 3COM y HPV1910 ********************************
#--------------------------------------------------------------------------------------------

def configurar_snmp_3com(ip, username, password, community_name, permiso):
    """
    Función para configurar SNMP en dispositivos 3Com y HPV1910 utilizando Paramiko.

    Parámetros:
        ip (number): Direccion IP del dispositivo.
        username (str): Usuario del dispositivo.
        password (str): Contrasena del dispositivo.
        comunity_name (str): Nombred de la comunidad.
        permiso (srt): Permiso de lectura {read} o escritura {write}. 
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password)  
        # Obtener un canal interactivo
        channel = ssh.invoke_shell()
        # Ingresamos en el modo de línea de comandos
        conexion_ssh.send_command(channel, "_cmdline-mode on", wait_time=2)
        conexion_ssh.interactive_send_command(
            channel,
            "Y",  # Confirmamos la pregunta para entrar en el modo de línea de comandos.
            "Please input password:",  # La cadena que esperamos antes de enviar la contraseña.
            "512900",  # Contraseña para el modo de línea de comandos.
            wait_time=2  # Tiempo de espera.
        )
        conexion_ssh.send_command(channel, "system-view", wait_time=2)
        conexion_ssh.send_command(channel, f"snmp-agent community {permiso} {community_name}", wait_time=2)
        ssh.close()
        print("Configuración de SNMP completada con éxito.")
    except Exception as e:
        print(f"Error al configurar SNMP en {ip}: {e}")
        ssh.close()

def configurar_snmp_acl_3com(ip, username, password, community_name, permiso, id_acl):
    """
    Función para configurar SNMP en dispositivos 3Com y HPV1910 utilizando Paramiko.

    Parámetros:
        ip (number): Direccion IP del dispositivo.
        username (str): Usuario del dispositivo.
        password (str): Contrasena del dispositivo.
        comunity_name (str): Nombred de la comunidad.
        permiso (srt): Permiso de lectura {read} o escritura {write}. 
        id_acl (number): Numero de la lista de acceso.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password)  
        # Obtener un canal interactivo
        channel = ssh.invoke_shell()
        # Ingresamos en el modo de línea de comandos
        conexion_ssh.send_command(channel, "_cmdline-mode on", wait_time=2)
        conexion_ssh.interactive_send_command(
            channel,
            "Y",  # Confirmamos la pregunta para entrar en el modo de línea de comandos.
            "Please input password:",  # La cadena que esperamos antes de enviar la contraseña.
            "512900",  # Contraseña para el modo de línea de comandos.
            wait_time=2  # Tiempo de espera.
        )
        conexion_ssh.send_command(channel, "system-view", wait_time=2)
        conexion_ssh.send_command(channel, f"snmp-agent community {permiso} {community_name} acl {id_acl}", wait_time=2)
        ssh.close()
        print("Configuración de SNMP completada con éxito.")
    except Exception as e:
        print(f"Error al configurar SNMP en {ip}: {e}")
        ssh.close()

#--------------------------------------------------------------------------------------------
#********************************* Configuracion TPLINK *************************************
#--------------------------------------------------------------------------------------------

def comandos_snmp(comunidad, permiso):
    """
    Genera un archivo de texto con comandos de configuración para SNMP.

    Parámetros:
        comunidad (str): El nombre de laa comunidad SNMP.
        permiso (srt): Permiso de lectura {read-only} o escritura {read-write}. 
    """
   
    nombre_archivo = r'/home/paola/Documentos/loginapp/topologia/inventarios/comandos_snmp.txt'
    comandos = dedent(f"""
    configure
    snmp-server community {comunidad} {permiso}
    """)

    # Escribimos los comandos en el archivo
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(comandos.strip())