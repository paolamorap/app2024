import paramiko
import conexion_ssh
from textwrap import dedent

#--------------------------------------------------------------------------------------------
#********************************* Configuracion CISCO **************************************
#--------------------------------------------------------------------------------------------

def configurar_vlan_cisco(connection, vlan_id, vlan_name):
    """
    Funcion para crear VLANs en dispositivos Cisco usando Netmiko.
    
    Parametros:
        connection: La conexión de Netmiko al dispositivo.
        vlan_id (number): Numero de VLAN.
        vlan_name (str): Nombre de la VLAN.
    """
    commands = [
        f'vlan {vlan_id}',
        f'name {vlan_name}',
        'exit',
    ]
    
    connection.send_config_set(commands)


#--------------------------------------------------------------------------------------------
#****************************** Configuracion HPA5120 ***************************************
#--------------------------------------------------------------------------------------------

def configurar_vlan_hp(connection, vlan_id, vlan_name):
    """
    Funcion para crear VLANs en dispositivos HPA5120 usando Netmiko.
    
    Parametros:
        connection: La conexión de Netmiko al dispositivo.
        vlan_id (number): Numero de VLAN.
        vlan_name (str): Nombre de la VLAN.

    """
    commands = [
        f'vlan {vlan_id}',
        f'name {vlan_name}',
        'quit',
    ]
    
    connection.send_config_set(commands)

#--------------------------------------------------------------------------------------------
#*******************************Configuracion 3COM y HPV1910 ********************************
#--------------------------------------------------------------------------------------------
def configurar_vlan_3com(ip, username, password, vlan_id, vlan_name):
    """
    Función para crear VLANs en dispositivos 3Com y HPV1910 utilizando Paramiko.

    Parámetros:
        ip (number): Direccion IP del dispositivo.
        username (str): Usuario del dispositivo.
        password (str): Contrasena del dispositivo.
        vlan_id (number): Numero de VLAN.
        vlan_name (str): Nombre de la VLAN.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password)  
        # Obtenemos un canal interactivo
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
        conexion_ssh.send_command(channel, f"vlan {vlan_id}", wait_time=2)
        conexion_ssh.send_command(channel, f"name {vlan_name}", wait_time=2)
        ssh.close()
        print("Creacion de VLAN completada con éxito.")
    except Exception as e:
        print(f"Error al crear VLAN en {ip}: {e}")
        ssh.close()


#--------------------------------------------------------------------------------------------
#********************************* Configuracion TPLINK *************************************
#--------------------------------------------------------------------------------------------

def comandos_vlan_tplink(vlan_id, vlan_name):
    """
    Genera un archivo de texto con comandos para crear VLANs en dispositivos TPLINK.

    Parámetros:
        vlan_id (number): Numero de VLAN.
        vlan_name (str): Nombre de la VLAN.
    """
    nombre_archivo = r'/home/paola/Documentos/loginapp/topologia/inventarios/comandos_vlan.txt'
    
    comandos = dedent(f"""
        configure
        vlan {vlan_id}
        name {vlan_name}
        exit
    """)

    # Escribimos los comandos en el archivo
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(comandos.strip())

