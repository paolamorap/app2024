import paramiko
from textwrap import dedent
from conexion_ssh import send_command, interactive_send_command
import os

#--------------------------------------------------------------------------------------------
#********************************* Configuracion CISCO **************************************
#--------------------------------------------------------------------------------------------

def configurar_logs_cisco(connection, servidorIP, trap, save_config=False):
    """
    Configura el servidor syslog y especifica los niveles de trap en dispositivos Cisco usando Netmiko.

    Esta función envía comandos para configurar la dirección IP del servidor syslog y establecer el nivel de severidad
    de los traps para la captura de logs.

    Parámetros:
        connection: Objeto de conexión Netmiko activo al dispositivo Cisco.
        servidorIP (str): Dirección IP del servidor syslog donde se enviarán los logs.
        trap (str): Nivel de severidad de los logs a capturar.
        save_config (bool): Si es True, ejecuta el comando para guardar la configuración en la memoria del dispositivo.

    Nota:
        Esta función no retorna un valor, pero ejecuta cambios en la configuración del dispositivo. Asegúrese de que
        los parámetros proporcionados son correctos y que la conexión al dispositivo está activa y estable.
    """
    commands = [
        f'logging host {servidorIP}',
        f'logging trap {trap}',
        'end',
    ]
    try:
        connection.send_config_set(commands)
        if save_config:
            connection.send_command('write memory')
        print(f"Configuración de logs completada exitosamente para el servidor {servidorIP}.")
    except Exception as e:
        print(f"Error al configurar logs en el dispositivo: {e}")



#--------------------------------------------------------------------------------------------
#****************************** Configuracion HPA5120 ***************************************
#--------------------------------------------------------------------------------------------

def configurar_logs_hp(connection, servidorIP, save_config=False):
    """
    Configura el servidor syslog en dispositivos HPA5120 usando Netmiko.

    Parámetros:
        connection: Objeto de conexión Netmiko activo al dispositivo HPA5120.
        servidorIP (str): Dirección IP del servidor syslog donde se enviarán los logs.
        save_config (bool): Si es True, ejecuta el comando para guardar la configuración en la memoria del dispositivo.

    Nota:
        Esta función no retorna un valor, pero ejecuta cambios en la configuración del dispositivo. Asegúrese de que
        los parámetros proporcionados son correctos y que la conexión al dispositivo está activa y estable.
    """
    commands = [
        f'info-center loghost {servidorIP}',
        'quit',
    ]
    try:
        connection.send_config_set(commands)
        if save_config:
            connection.send_command('save force')
        print(f"Configuración de logs completada exitosamente para el servidor {servidorIP}.")
    except Exception as e:
        print(f"Error al configurar logs en el dispositivo: {e}")


#--------------------------------------------------------------------------------------------
#*******************************Configuracion 3COM y HPV1910 ********************************
#--------------------------------------------------------------------------------------------

def configurar_logs_3com(ip, username, password, servidorIP, save_config=False):
    """
    Configura el servidor syslog en dispositivos 3Com y HPV1910 utilizando Paramiko para la conexión SSH.

    Parámetros:
        ip (str): Dirección IP del dispositivo.
        username (str): Usuario del dispositivo para la autenticación SSH.
        password (str): Contraseña del dispositivo.
        servidorIP (str): Dirección IP del servidor syslog donde se enviarán los logs.

    Nota:
        Esta función no retorna un valor, pero ejecuta cambios en la configuración del dispositivo. Asegúrese de que
        los parámetros proporcionados son correctos y que la conexión SSH al dispositivo está activa y estable.
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
        send_command(channel, f"info-center loghost {servidorIP}", wait_time=2)
        send_command(channel, f"quit", wait_time=2)

        # Guardar la configuración si se indica
        if save_config:
            send_command(channel, "save", wait_time=2)
            interactive_send_command(channel, "Y", "Are you sure to overwrite the current configuration", "", wait_time=2)
        print("Configuración de LOGS completada con éxito.")
    except Exception as e:
        print(f"Error al configurar LOGS en {ip}: {e}")
    finally:
        ssh.close()



#--------------------------------------------------------------------------------------------
#********************************* Configuracion TPLINK *************************************
#--------------------------------------------------------------------------------------------

def comandos_logs_tplink(servidorIP, trap, archivo_destino=None):
    """
    Genera un archivo de texto con comandos para configurar LOGS en dispositivos TPLINK,
    almacenando los comandos en un archivo txt.

    Esta función envía comandos para configurar la dirección IP del servidor syslog y establecer el nivel de severidad
    de los traps para la captura de logs.

    Parámetros:
        servidorIP (str): Dirección IP del servidor syslog donde se enviarán los logs.
        trap (str): Nivel de severidad de los logs a capturar.
        archivo_destino (str, opcional): Ruta completa del archivo donde se guardarán los comandos.
                                         Si no se proporciona, se usa una ruta predeterminada.

    Retorna:
        str: Ruta al archivo generado con los comandos.
    """
    # Ruta predeterminada si no se especifica una
    if archivo_destino is None:
        archivo_destino = '/home/paola/Documentos/app2024/modulo_automatizacion/comandos/comandos_logs.txt'
    
    comandos = dedent(f"""
        configure
        logging host index 2 {servidorIP} {trap}
        exit
    """)

    # Aseguramos que el directorio donde se guardará el archivo exista
    os.makedirs(os.path.dirname(archivo_destino), exist_ok=True)

    # Escribimos los comandos en el archivo
    with open(archivo_destino, 'w') as archivo:
        archivo.write(comandos.strip())
    
    return archivo_destino