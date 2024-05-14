import paramiko
from textwrap import dedent
from conexion_ssh import send_command, interactive_send_command
import os
#--------------------------------------------------------------------------------------------
#********************************* Configuracion CISCO **************************************
#--------------------------------------------------------------------------------------------

def configurar_acl_cisco(connection, id_list, ip_red, mascara_wildcard, save_config=False):
    """
    Configura una lista de acceso (ACL) en dispositivos Cisco para permitir el tráfico desde una dirección IP específica
    utilizando una conexión Netmiko.

    Parámetros:
        connection (Netmiko Connection): Conexión activa al dispositivo Cisco.
        id_list (int): ID de la lista de acceso.
        ip_red (str): IP de la red a la que se le da acceso.
        mascara_wildcard (str): Máscara wildcard asociada a la IP de la red.
        save_config (bool): Indica si se debe guardar la configuración permanentemente en el dispositivo.
                            El valor predeterminado es False.

    Nota:
        Esta función no retorna un valor, pero ejecuta cambios en la configuración del dispositivo.
        Asegúrese de que los parámetros proporcionados son correctos y que la conexión al dispositivo
        está activa y estable.
    
    """
    commands = [
        f"access-list {id_list} permit {ip_red} {mascara_wildcard}",
        'end',
    ]
    try:
        connection.send_config_set(commands)
        if save_config:
            connection.send_command('write memory')
        print(f"Access List {id_list} creada con éxito en la red {ip_red}.")
    except Exception as e:
        print(f"Error al crear ACL en la red {ip_red}: {e}")


#--------------------------------------------------------------------------------------------
#****************************** Configuracion HPA5120 ***************************************
#--------------------------------------------------------------------------------------------

def configurar_acl_hp(connection, n_regla, id_list, ip_red, mascara_wildcard, save_config=False):
    """
    Configura una lista de acceso (ACL) en dispositivos HPA5120 para permitir tráfico desde una dirección IP específica
    utilizando una conexión Netmiko.

    Parámetros:
        connection (Netmiko Connection): Conexión activa al dispositivo HPA5120.
        n_regla (int): Número de la regla dentro de la ACL.
        id_list (int): ID de la lista de acceso.
        ip_red (str): IP de la red a la que se le da acceso.
        mascara_wildcard (str): Máscara wildcard asociada a la IP de la red.
        save_config (bool): Indica si se debe guardar la configuración permanentemente en el dispositivo.
                            El valor predeterminado es False.

    Nota:
        Esta función no retorna un valor, pero ejecuta cambios en la configuración del dispositivo.
        Asegúrese de que los parámetros proporcionados son correctos y que la conexión al dispositivo
        está activa y estable.

    """
    commands = [
        f"acl number {id_list}",
        f"rule {n_regla} permit source {ip_red} {mascara_wildcard}",
        'quit',
    ]
    try:
        connection.send_config_set(commands)
        if save_config:
            connection.send_command('save force')  # Comando para guardar la configuración en dispositivos HP
        print(f"Access List {id_list} creada con éxito en la red {ip_red}.")
    except Exception as e:
        print(f"Error al crear ACL en la red {ip_red}: {e}")


#--------------------------------------------------------------------------------------------
#*******************************Configuracion 3COM y HPV1910 ********************************
#--------------------------------------------------------------------------------------------

def configurar_acl_3com(ip, username, password, n_regla, id_list, ip_red, mascara_wildcard, save_config=False):
    """
    Configura una lista de acceso (ACL) en dispositivos 3Com y HPV1910 para permitir tráfico desde una dirección IP específica
    utilizando Paramiko para la conexión SSH.

    Parámetros:
        ip (str): Dirección IP del dispositivo.
        username (str): Usuario del dispositivo.
        password (str): Contraseña del dispositivo.
        n_regla (int): Número de la regla dentro de la ACL.
        id_list (int): ID de la lista de acceso.
        ip_red (str): IP de la red a la que se le da acceso.
        mascara_wildcard (str): Máscara wildcard asociada a la IP de la red.
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
            "Y",  # Confirmamos la pregunta para entrar en el modo de línea de comandos.
            "Please input password:",  # La cadena que esperamos antes de enviar la contraseña.
            "512900",  # Contraseña para el modo de línea de comandos.
            wait_time=2  # Tiempo de espera.
        )
        send_command(channel, "system-view", wait_time=2)
        send_command(channel, f"acl number {id_list}", wait_time=2)
        send_command(channel, f"rule {n_regla} permit source {ip_red} {mascara_wildcard}", wait_time=2)
        send_command(channel, f"quit", wait_time=2)

        # Guardar la configuración si se indica
        if save_config:
            send_command(channel, "save", wait_time=2)
            interactive_send_command(channel, "Y", "Are you sure to overwrite the current configuration", "", wait_time=2)

        print(f"Access List {id_list} creada con éxito en la red {ip_red}.")
    except Exception as e:
        print(f"Error al crear ACL en {ip}: {e}")
    finally:
        ssh.close()


#--------------------------------------------------------------------------------------------
#********************************* Configuracion TPLINK *************************************
#--------------------------------------------------------------------------------------------

def comandos_acl_tplink(n_regla, id_list, ip_red, mascara_wildcard):
    """
    Genera un archivo de texto con comandos para configurar una lista de acceso (ACL) en dispositivos TPLINK,
    almacenando los comandos en un archivo txt.

    Esta función crea una cadena de comandos necesarios para configurar una lista de acceso (ACL)en un dispositivos. 
    Los comandos se escriben en un archivo de texto en la ruta especificada. Si no se proporciona una ruta, se utiliza 
    una ruta predeterminada.

    Parámetros:
        n_regla (int): Número de la regla.
        id_list (int): ID de la lista de acceso.
        ip_red (str): IP de la red a la que se le da acceso.
        mascara_wildcard (str): Máscara wildcard asociada a la IP de la red.

    Retorna:
        str: Ruta al archivo generado con los comandos.
    """

    # Ruta predeterminada si no se especifica una
    if archivo_destino is None:
        archivo_destino = '/home/paola/Documentos/app2024/modulo_automatizacion/comandos/comandos_acl.txt'
    
    comandos = dedent(f"""
    configure
    access-list create {id_list}
    access-list ip {id_list} rule {n_regla} permit logging disable sip {ip_red} sip-mask {mascara_wildcard}
    end
    """)
    
    # Aseguramos que el directorio donde se guardará el archivo exista
    os.makedirs(os.path.dirname(archivo_destino), exist_ok=True)

    # Escribimos los comandos en el archivo
    with open(archivo_destino, 'w') as archivo:
        archivo.write(comandos.strip())
    
    return archivo_destino