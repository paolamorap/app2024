import paramiko
import conexion_ssh
from textwrap import dedent

#--------------------------------------------------------------------------------------------
#********************************* Configuracion CISCO **************************************
#--------------------------------------------------------------------------------------------

def configurar_logs_cisco(connection, servidorIP, trap):
    """
    Funcion para configurar LOGS en dispositivos Cisco usando Netmiko.
    
    Parametros:
        connection: La conexión de Netmiko al dispositivo.
        servidorIP: Direccion IP del servidor syslog
        trap: Tipos de logs 
    """
    commands = [
        f'logging host {servidorIP}',
        f'loggin trap {trap}',
        'exit',
    ]
    
    connection.send_config_set(commands)


#--------------------------------------------------------------------------------------------
#****************************** Configuracion HPA5120 ***************************************
#--------------------------------------------------------------------------------------------

def configurar_logs_hp(connection, servidorIP):
    """
    Funcion para configurar LOGS en dispositivos HPA5120 usando Netmiko.
    
    Parametros:
        connection: La conexión de Netmiko al dispositivo.
        servidorIP: Direccion IP del servidor syslog.
        trap: Tipos de logs.
    """
    commands = [
        f'infor-center loghost {servidorIP}',
        'quit',
    ]
    
    connection.send_config_set(commands)

#--------------------------------------------------------------------------------------------
#*******************************Configuracion 3COM y HPV1910 ********************************
#--------------------------------------------------------------------------------------------

def configurar_logs_3com(ip, username, password, servidorIP):
    """
    Funcion para configurar LOGS en dispositivos 3Com y HPV1910 usando Paramiko.
    
    Parametros:
        ip (number): Direccion IP del dispositivo.
        username (str): Usuario del dispositivo.
        password (str): Contrasena del dispositivo.
        servidorIP: Direccion IP del servidor syslog.
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
            "512900",  # La contraseña para el modo de línea de comandos.
            wait_time=2  # Tiempo de espera.
        )
        conexion_ssh.send_command(channel, "system-view", wait_time=2)
        conexion_ssh.send_command(channel, f"infor-center loghost {servidorIP}", wait_time=2)
        ssh.close()
        print("Configuracion de LOGS completada con éxito.")
    except Exception as e:
        print(f"Error al configurar LOGS en {ip}: {e}")
        ssh.close()


#--------------------------------------------------------------------------------------------
#********************************* Configuracion TPLINK *************************************
#--------------------------------------------------------------------------------------------

def comandos_logs_tplink(servidorIP, trap):
    """
    Genera un archivo de texto con comandos para configurar LOGS en dispositivos TPLINK.

    Parámetros:
        servidorIP: Direccion IP del servidor syslog.
        trap: Tipos de logs.
    """
    nombre_archivo = r'/home/paola/Documentos/loginapp/topologia/inventarios/comandos_logs.txt'
        
    comandos = dedent(f"""
        configure
        logging host index 2 {servidorIP} {trap}
    """)

    # Escribimos los comandos en el archivo
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(comandos.strip())

