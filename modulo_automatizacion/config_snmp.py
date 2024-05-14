import paramiko
from conexion_ssh import send_command, interactive_send_command
from textwrap import dedent
import os


#--------------------------------------------------------------------------------------------
#********************************* Configuracion CISCO **************************************
#--------------------------------------------------------------------------------------------

def configurar_snmp_cisco(connection, community_name, permiso, save_config=False):
    """
    Configura SNMP en dispositivos Cisco utilizando una conexión Netmiko.

    Esta función envía comandos para establecer la configuración SNMP de una comunidad especificada con un nivel de permiso
    determinado (lectura o escritura) en dispositivos Cisco. Es útil para gestionar el acceso SNMP a dispositivos de red.

    Parámetros:
        connection: Objeto de conexión Netmiko activo al dispositivo Cisco.
        community_name (str): Nombre de la comunidad SNMP a configurar.
        permiso (str): Permiso asignado a la comunidad SNMP, puede ser 'RO' para solo lectura o 'RW' para lectura y escritura.
        save_config (bool): Indica si se debe guardar la configuración permanentemente en el dispositivo.
                            El valor predeterminado es False.

    Nota:
        Esta función no retorna un valor, pero ejecuta cambios en la configuración del dispositivo. Asegúrese de que
        los parámetros proporcionados son correctos y que la conexión al dispositivo está activa y estable.
    """
    commands = [
        f"snmp-server community {community_name} {permiso}",
        'end',
    ]
    try:
        connection.send_config_set(commands)
        if save_config:
            connection.send_command('write memory')
        print(f"Configuración SNMP con comunidad '{community_name}' y permiso '{permiso}' completada exitosamente.")
    except Exception as e:
        print(f"Error al configurar SNMP en el dispositivo: {e}")


def configurar_snmp_acl_cisco(connection, community_name, permiso, id_acl, save_config=False):
    """
    Configura SNMP con una lista de acceso en dispositivos Cisco utilizando una conexión Netmiko.

    Esta función establece la configuración SNMP de una comunidad específica con un nivel de permiso determinado
    y restringe el acceso usando una lista de acceso (ACL) especificada por el usuario. Es útil para gestionar
    el acceso SNMP a dispositivos de red de manera segura y controlada.

    Parámetros:
        connection: Objeto de conexión Netmiko activo al dispositivo Cisco.
        community_name (str): Nombre de la comunidad SNMP a configurar.
        permiso (str): Permiso asignado a la comunidad SNMP, puede ser 'RO' (solo lectura) o 'RW' (lectura y escritura).
        id_acl (int): Número identificador de la lista de acceso (ACL) que se aplicará a la comunidad SNMP.
        save_config (bool): Indica si se debe guardar la configuración permanentemente en el dispositivo.
                            El valor predeterminado es False.

    Nota:
        Esta función no retorna un valor, pero ejecuta cambios en la configuración del dispositivo.
        Asegúrese de que los parámetros proporcionados son correctos y que la conexión al dispositivo
        está activa y estable.
    """
    commands = [
        f"snmp-server community {community_name} {permiso} {id_acl}",
        'end',
    ]
    try:
        connection.send_config_set(commands)
        if save_config:
            connection.send_command('write memory')
        print(f"Configuración SNMP con comunidad '{community_name}', permiso '{permiso}', y ACL '{id_acl}' completada exitosamente.")
    except Exception as e:
        print(f"Error al configurar SNMP con ACL en el dispositivo: {e}")


#--------------------------------------------------------------------------------------------
#****************************** Configuracion HPA5120 ***************************************
#--------------------------------------------------------------------------------------------

def configurar_snmp_hp(connection, community_name, permiso, save_config=False):
    """
    Configura SNMP en dispositivos HPA5120 utilizando una conexión Netmiko.

    Esta función envía comandos para establecer la configuración SNMP de una comunidad especificada con un nivel de permiso
    determinado (lectura o escritura) en dispositivos HPA5120. Es útil para gestionar el acceso SNMP a dispositivos de red.

    Parámetros:
        connection: Objeto de conexión Netmiko activo al dispositivo HPA5120.
        community_name (str): Nombre de la comunidad SNMP a configurar.
        permiso (str): Permiso asignado a la comunidad SNMP, puede ser 'read' para solo lectura o 'write' para lectura y escritura.
        save_config (bool): Indica si se debe guardar la configuración permanentemente en el dispositivo.
                            El valor predeterminado es False.

    Nota:
        Esta función no retorna un valor, pero ejecuta cambios en la configuración del dispositivo.
        Asegúrese de que los parámetros proporcionados son correctos y que la conexión al dispositivo
        está activa y estable.
    """
    commands = [
        f"snmp-agent community {permiso} {community_name}",
        'quit',
    ]
    try:
        connection.send_config_set(commands)
        if save_config:
            connection.send_command('save force')  # Comando para guardar la configuración en dispositivos HP
        print(f"Configuración SNMP con comunidad '{community_name}' y permiso '{permiso}' completada exitosamente.")
    except Exception as e:
        print(f"Error al configurar SNMP en el dispositivo: {e}")


def configurar_snmp_acl_hp(connection, community_name, permiso, id_acl, save_config=False):
    """
    Configura SNMP con una lista de acceso en dispositivos HPA5120 utilizando una conexión Netmiko.

    Esta función establece la configuración SNMP de una comunidad específica con un nivel de permiso determinado
    y restringe el acceso usando una lista de acceso (ACL) especificada por el usuario. Es útil para gestionar
    el acceso SNMP a dispositivos de red de manera segura y controlada.

    Parámetros:
        connection: Objeto de conexión Netmiko activo al dispositivo HPA5120.
        community_name (str): Nombre de la comunidad SNMP a configurar.
        permiso (str): Permiso asignado a la comunidad SNMP, puede ser 'read' (solo lectura) o 'write' (lectura y escritura).
        id_acl (int): Número identificador de la lista de acceso (ACL) que se aplicará a la comunidad SNMP.
        save_config (bool): Indica si se debe guardar la configuración permanentemente en el dispositivo.
                            El valor predeterminado es False.

    Nota:
        Esta función no retorna un valor, pero ejecuta cambios en la configuración del dispositivo.
        Asegúrese de que los parámetros proporcionados son correctos y que la conexión al dispositivo
        está activa y estable.
    """
    commands = [
        f"snmp-agent community {permiso} {community_name} acl {id_acl}",
        'quit',
    ]
    try:
        connection.send_config_set(commands)
        if save_config:
            connection.send_command('save force')  # Comando para guardar la configuración en dispositivos HP
        print(f"Configuración SNMP con comunidad '{community_name}', permiso '{permiso}', y ACL '{id_acl}' completada exitosamente.")
    except Exception as e:
        print(f"Error al configurar SNMP con ACL en el dispositivo: {e}")



#--------------------------------------------------------------------------------------------
#*******************************Configuracion 3COM y HPV1910 ********************************
#--------------------------------------------------------------------------------------------

def configurar_snmp_3com(ip, username, password, community_name, permiso, save_config=False):
    """
    Configura SNMP en dispositivos 3Com y HPV1910 utilizando Paramiko para la conexión SSH.

    Esta función establece la configuración SNMP de una comunidad específica con un nivel de permiso determinado
    (lectura o escritura) en dispositivos 3Com y HPV1910.

    Parámetros:
        ip (str): Dirección IP del dispositivo.
        username (str): Nombre de usuario para la autenticación SSH.
        password (str): Contraseña del usuario.
        community_name (str): Nombre de la comunidad SNMP a configurar.
        permiso (str): Permiso asignado a la comunidad SNMP, puede ser 'read' para solo lectura o 'write' para lectura y escritura.
        save_config (bool): Indica si se debe guardar la configuración permanentemente en el dispositivo.
                            El valor predeterminado es False.
    Nota:
        Esta función no retorna un valor, pero ejecuta cambios en la configuración del dispositivo.
        Asegúrese de que los parámetros proporcionados son correctos y que la conexión al dispositivo
        está activa y estable.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password)  
        channel = ssh.invoke_shell()
        send_command(channel, "_cmdline-mode on", wait_time=2)
        interactive_send_command(
            channel,
            "Y",
            "Please input password:",
            "512900",
            wait_time=2
        )
        send_command(channel, "system-view", wait_time=2)
        send_command(channel, f"snmp-agent community {permiso} {community_name}", wait_time=2)
        send_command(channel, f"quit", wait_time=2)

        # Guardar la configuración si se indica
        if save_config:
            send_command(channel, "save", wait_time=2)
            interactive_send_command(channel, "Y", "Are you sure to overwrite the current configuration", "", wait_time=2)

        print(f"Configuración SNMP con comunidad '{community_name}' y permiso '{permiso}' completada exitosamente.")
    except Exception as e:
        print(f"Error al configurar SNMP en {ip}: {e}")
    finally:
        ssh.close()


def configurar_snmp_acl_3com(ip, username, password, community_name, permiso, id_acl, save_config=False):
    """
    Configura SNMP con una lista de acceso en dispositivos 3Com y HPV1910 utilizando Paramiko para la conexión SSH.

    Esta función establece la configuración SNMP de una comunidad específica con un nivel de permiso determinado
    y restringe el acceso usando una lista de acceso (ACL) especificada por el usuario.

    Parámetros:
        ip (str): Dirección IP del dispositivo.
        username (str): Nombre de usuario para la autenticación SSH.
        password (str): Contraseña del usuario.
        community_name (str): Nombre de la comunidad SNMP a configurar.
        permiso (str): Permiso asignado a la comunidad SNMP, puede ser 'read' (solo lectura) o 'write' (lectura y escritura).
        id_acl (int): Número identificador de la lista de acceso (ACL) que se aplicará a la comunidad SNMP.
        save_config (bool): Indica si se debe guardar la configuración permanentemente en el dispositivo.
                            El valor predeterminado es False.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password)  
        channel = ssh.invoke_shell()
        send_command(channel, "_cmdline-mode on", wait_time=2)
        interactive_send_command(
            channel,
            "Y",
            "Please input password:",
            "512900",
            wait_time=2
        )
        send_command(channel, "system-view", wait_time=2)
        send_command(channel, f"snmp-agent community {permiso} {community_name} acl {id_acl}", wait_time=2)

        # Guardar la configuración si se indica
        if save_config:
            send_command(channel, "save", wait_time=2)
            interactive_send_command(channel, "Y", "Are you sure to overwrite the current configuration", "", wait_time=2)
            
        print(f"Configuración SNMP con comunidad '{community_name}', permiso '{permiso}', y ACL '{id_acl}' completada exitosamente.")
    except Exception as e:
        print(f"Error al configurar SNMP con ACL en {ip}: {e}")
    finally:
        ssh.close()


#--------------------------------------------------------------------------------------------
#********************************* Configuracion TPLINK *************************************
#--------------------------------------------------------------------------------------------

def comandos_snmp_tplink(comunidad, permiso, archivo_destino=None):
    """
    Genera un archivo de texto con comandos para configurar SNMP en un dispositivo TPLINK,
    almacenando los comandos en un archivo txt.

    Esta función crea una cadena de comandos necesarios para configurar SNMP en un dispositivo TPLINK,
    utilizando una comunidad y permisos especificados. Los comandos se escriben en un archivo de texto
    en la ruta especificada. Si no se proporciona una ruta, se utiliza una ruta predeterminada.

    Parámetros:
        comunidad (str): Nombre de la comunidad SNMP a configurar.
        permiso (str): Permiso asignado a la comunidad SNMP, puede ser 'read-only' para solo lectura
                       o 'read-write' para lectura y escritura.
        archivo_destino (str, opcional): Ruta completa del archivo donde se guardarán los comandos.
                                         Si no se proporciona, se usa una ruta predeterminada.

    Retorna:
        str: La ruta del archivo donde se guardaron los comandos.
    """
    # Ruta predeterminada si no se especifica una
    if archivo_destino is None:
        archivo_destino = '/home/paola/Documentos/app2024/modulo_automatizacion/comandos/comandos_snmp.txt'

    comandos = dedent(f"""
        configure
        snmp-server community {comunidad} {permiso}
        end
    """)

    # Aseguramos que el directorio donde se guardará el archivo exista
    os.makedirs(os.path.dirname(archivo_destino), exist_ok=True)

    # Escribimos los comandos en el archivo
    with open(archivo_destino, 'w') as archivo:
        archivo.write(comandos.strip())
    
    return archivo_destino