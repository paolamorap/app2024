import paramiko
import os
from textwrap import dedent
from conexion_ssh import send_command, interactive_send_command


#--------------------------------------------------------------------------------------------
#********************************* Configuracion CISCO **************************************
#--------------------------------------------------------------------------------------------

def configurar_vlan_cisco(connection, vlan_id, vlan_name, save_config=False):
    """
    Crea una VLAN en dispositivos Cisco utilizando una conexión Netmiko y opcionalmente guarda la configuración.

    Parámetros:
        connection: Objeto de conexión Netmiko activo al dispositivo Cisco.
        vlan_id (int): Número de la VLAN que se desea configurar.
        vlan_name (str): Nombre descriptivo para la VLAN.
        save_config (bool): Si es True, guarda la configuración en la memoria permanente del dispositivo.

    """
    commands = [
        f'vlan {vlan_id}',
        f'name {vlan_name}',
        'end',
    ]
    
    try:
        connection.send_config_set(commands)
        if save_config:
            connection.send_command('write memory')
        print(f"VLAN {vlan_id} - '{vlan_name}' configurada y guardada exitosamente.")
    except Exception as e:
        print(f"Error al configurar y guardar VLAN: {e}")




#--------------------------------------------------------------------------------------------
#****************************** Configuracion HPA5120 ***************************************
#--------------------------------------------------------------------------------------------

def configurar_vlan_hp(connection, vlan_id, vlan_name, save_config=False):
    """
    Crea una VLAN en dispositivos HP A5120 utilizando una conexión Netmiko.
    
    Esta función envía una serie de comandos a un dispositivo HP A5120 para configurar una VLAN con un ID y nombre específicos.
    Los comandos se envían en modo de configuración, y se puede optar por guardar los cambios permanentemente en la memoria del dispositivo.

    Parámetros:
        connection: Objeto de conexión Netmiko activo al dispositivo HP.
        vlan_id (int): Número de la VLAN que se desea configurar.
        vlan_name (str): Nombre descriptivo para la VLAN.
        save_config (bool): Si es True, ejecuta el comando para guardar la configuración en la memoria del dispositivo.
    """
    commands = [
        f'vlan {vlan_id}',
        f'name {vlan_name}',
        'quit',  # Salir del contexto de configuración de VLAN
    ]
    
    try:
        connection.send_config_set(commands)
        if save_config:
            connection.send_command('save force')  # Comando para guardar la configuración en dispositivos HP
        print(f"VLAN {vlan_id} - '{vlan_name}' configurada exitosamente.")
    except Exception as e:
        print(f"Error al configurar VLAN: {e}")


#--------------------------------------------------------------------------------------------
#*******************************Configuracion 3COM y HPV1910 ********************************
#--------------------------------------------------------------------------------------------


def configurar_vlan_3com(ip, username, password, vlan_id, vlan_name, save_config=False):
    """
    Crea una VLAN en dispositivos 3Com y HPV1910 utilizando la biblioteca Paramiko para manejar conexiones SSH y
    opcionalmente guarda la configuración en la memoria permanente del dispositivo.

    Parámetros:
        ip (str): Dirección IP del dispositivo.
        username (str): Nombre de usuario para la autenticación SSH.
        password (str): Contraseña del usuario.
        vlan_id (int): Número identificador de la VLAN a crear.
        vlan_name (str): Nombre descriptivo para la nueva VLAN.
        save_config (bool): Indica si se debe guardar la configuración permanentemente en el dispositivo.
                            El valor predeterminado es False.

    Ejemplo de uso:
        configurar_vlan_3com('192.168.1.1', 'admin', 'adminpass', 10, 'GuestVLAN')
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password)
        channel = ssh.invoke_shell()

        # Ingresamos en el modo de línea de comandos y configuramos la VLAN
        send_command(channel, "_cmdline-mode on", wait_time=2)
        respuesta = interactive_send_command(
            channel, "Y", "Please input password:", "512900", wait_time=2
        )
        if "Error" in respuesta:
            raise Exception("No se pudo ingresar al modo de línea de comandos.")

        send_command(channel, "system-view", wait_time=2)
        send_command(channel, f"vlan {vlan_id}", wait_time=2)
        send_command(channel, f"name {vlan_name}", wait_time=2)

        # Guardar la configuración si se indica
        if save_config:
            send_command(channel, "save", wait_time=2)
            interactive_send_command(channel, "Y", "Are you sure to overwrite the current configuration", "", wait_time=2)

        print(f"VLAN {vlan_id} - '{vlan_name}' configurada exitosamente en el dispositivo {ip}.")

    except Exception as e:
        print(f"Error al crear VLAN en {ip}: {e}")
    finally:
        # Asegurar que la conexión SSH siempre se cierre
        ssh.close()


#--------------------------------------------------------------------------------------------
#********************************* Configuracion TPLINK *************************************
#--------------------------------------------------------------------------------------------

def comandos_vlan_tplink(vlan_id, vlan_name, archivo_destino=None):
    """
    Genera un archivo de texto con comandos para configurar VLANs en dispositivos TPLink y lo almacena en una ubicación especificada.

    Esta función crea una cadena de comandos necesarios para configurar una VLAN específica en dispositivos TPLink y
    escribe esos comandos en un archivo de texto en la ruta especificada. Si no se especifica una ruta, se utiliza una ruta predeterminada.

    Parámetros:
        vlan_id (int): Número de la VLAN que se desea configurar.
        vlan_name (str): Nombre descriptivo para la VLAN.
        archivo_destino (str, opcional): Ruta completa del archivo donde se guardarán los comandos. Si no se proporciona, se usa una ruta predeterminada.

    Retorna:
        str: La ruta del archivo donde se guardaron los comandos.
    """
    # Ruta predeterminada si no se especifica una
    if archivo_destino is None:
        archivo_destino = '/home/paola/Documentos/app2024/modulo_automatizacion/comandos/comandos_vlan.txt'

    comandos = dedent(f"""
        configure
        vlan {vlan_id}
        name {vlan_name}
        exit
        wr
    """)

    # Aseguramos que el directorio donde se guardará el archivo exista
    os.makedirs(os.path.dirname(archivo_destino), exist_ok=True)

    # Escribimos los comandos en el archivo
    with open(archivo_destino, 'w') as archivo:
        archivo.write(comandos.strip())
    
    return archivo_destino

 

