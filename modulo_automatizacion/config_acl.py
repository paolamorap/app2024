import paramiko
import conexion_ssh
from textwrap import dedent
#--------------------------------------------------------------------------------------------
#********************************* Configuracion CISCO **************************************
#--------------------------------------------------------------------------------------------

def configurar_acl_cisco(connection, id_list, ip_red, mascara_wildcard):
    """
    Función para configurar ACL en dispositivos CISCO utilizando Netmiko.

    Parámetros:
        n_regla (number): Numero de la regla.
        id_list (number): ID de la lista de acceso.
        ip_red (number): IP de la red a la que se le da acceso.
        mascara_wildcard (number): Mascara Wircard
    """
    commands = [
        f"access-list {id_list} permit {ip_red} {mascara_wildcard}",
    ]
    connection.send_config_set(commands)

#--------------------------------------------------------------------------------------------
#****************************** Configuracion HPA5120 ***************************************
#--------------------------------------------------------------------------------------------

def configurar_acl_hp(connection, n_regla, id_list, ip_red, mascara_wildcard):
    """
    Función para configurar ACL en dispositivos HPA5120 utilizando Netmiko.

    Parámetros:
        n_regla (number): Numero de la regla.
        id_list (number): ID de la lista de acceso.
        ip_red (number): IP de la red a la que se le da acceso.
        mascara_wildcard (number): Mascara Wircard
    """

    commands = [
        f"acl number {id_list}",
        f"rule {n_regla} permit source {ip_red} {mascara_wildcard}",
    ]
    connection.send_config_set(commands)

#--------------------------------------------------------------------------------------------
#*******************************Configuracion 3COM y HPV1910 ********************************
#--------------------------------------------------------------------------------------------

def configurar_acl_3com(ip, username, password, n_regla, id_list, ip_red, mascara_wildcard):
    """
    Función para configurar ACL en dispositivos 3Com y HPV1910 utilizando Paramiko.

    Parámetros:
        ip (number): Direccion IP del dispositivo.
        username (str): Usuario del dispositivo.
        password (str): Contrasena del dispositivo.
        n_regla (number): Numero de la regla.
        id_list (number): ID de la lista de acceso.
        ip_red (number): IP de la red a la que se le da acceso.
        mascara_wircard (number): Mascara Wircard
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
        conexion_ssh.send_command(channel, f"acl number {id_list}", wait_time=2)
        conexion_ssh.send_command(channel, f"rule {n_regla} permit source {ip_red} {mascara_wildcard}", wait_time=2)
        ssh.close()
        print("Configuración de SNMP completada con éxito.")
    except Exception as e:
        print(f"Error al configurar SNMP en {ip}: {e}")
        ssh.close()

#--------------------------------------------------------------------------------------------
#********************************* Configuracion TPLINK *************************************
#--------------------------------------------------------------------------------------------

def comandos_acl_tplink(n_regla, id_list, ip_red, mascara_wircard ):
    """
    Genera un archivo de texto con comandos de configuración para configuracion ACL

    Parámetros:
        n_regla (number): Numero de la regla.
        id_list (number): ID de la lista de acceso.
        ip_red (number): IP de la red a la que se le da acceso.
        mascara_wircard (number): Mascara Wircard
    """

    nombre_archivo = r'/home/paola/Documentos/loginapp/topologia/inventarios/comandos_acl.txt'
    comandos = dedent(f"""
    configure
    access-list create {id_list}
    access-list ip {id_list} rule {n_regla} permit logging disable sip {ip_red} sip-mask {mascara_wircard}
    """)

    # Escribimos los comandos en el archivo
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(comandos.strip())