import paramiko
import conexion_ssh
from textwrap import dedent

#--------------------------------------------------------------------------------------------
#********************************* Configuracion CISCO **************************************
#--------------------------------------------------------------------------------------------

def configurar_stpMode_cisco(connection, region_name, modo):
    """
    Funcion para activar modo STP en dispositivos Cisco usando Netmiko.
    
    Parametros:
        connection: La conexión de Netmiko al dispositivo.
        modo: El modo de STP deseado (pvst, rapid-pvst o mst).
        region_name: El nombre de la región MST.
    """
    commands = [
        f'spanning-tree mode {modo}',
    ]
    
    if modo == 'mst':
        commands.extend([
            'spanning-tree mst configuration',
            f'name {region_name}',
            'exit',
        ])
        
    commands.append('end')
    
    connection.send_config_set(commands)

def configurar_stpPrioridad_cisco(connection, prioridad, vlaniD):
    """
    Funcion para configurar la prioridad STP en dispositivos Cisco usando Netmiko.
    
    Parametros:
        connection: La conexión de Netmiko al dispositivo.
        prioridad: Numero de prioridad (Rango de 0 - 61440).
    """
    commands = [
        f'spanning-tree vlan {vlaniD} priority {prioridad}',
        f'end',
    ]
    
    connection.send_config_set(commands)

#--------------------------------------------------------------------------------------------
#****************************** Configuracion HPA5120 ***************************************
#--------------------------------------------------------------------------------------------

def configurar_stpMode_hp(connection, region_name, modo):
    """
    Funcion para activar el modo STP en dispositivos HPA5120 usando Netmiko.
    
    Parametros:
        connection: La conexión de Netmiko al dispositivo.
        region_name: El nombre de la región MST.
        modo: El modo de STP deseado (STP, RSTP o MSTP).
    """
    commands = [
        f'stp mode {modo}'
    ]
    
    if modo == 'mst':
        commands.extend([
            'stp region-configuration',
            f'region-name {region_name}',
            'active region-configuration',
        ])
        
    commands.extend([
        'stp enable',
        'exit',
    ])
    
    connection.send_config_set(commands)

def configurar_stpPrioridad_hp(connection, instance, modo, prioridad, vlan):
    """
    Funcion para configurar la prioridad STP en dispositivos HPA5120 usando Netmiko.
    
    Parametros:
        connection: La conexión de Netmiko al dispositivo.
        prioridad: Numero de prioridad (Rango de 0 - 61440).
        instancia: Numero de instancia (0 por defecto y agrupa todas las VLANS que no han sido asignadas a otras vlans)
        vlan: Rango de VLANS
    """

    commands = [
    ]
    
    if modo == 'stp' or modo == 'rstp':
        commands.extend([
            f'stp priority {prioridad}',
        ])
    elif modo == 'pvst':
        commands.extend([
            f'stp vlan {vlan} priority {prioridad}',
        ])
    elif modo == 'mstp':
        commands.extend([
            f'stp instance {instance} priority {prioridad}',
        ])

    commands.extend([
        'exit',
    ])

    
    connection.send_config_set(commands)

#--------------------------------------------------------------------------------------------
#*******************************Configuracion 3COM y HPV1910 ********************************
#--------------------------------------------------------------------------------------------

def configurar_STP_3com(ip, username, password, region_name, modo):
    """
    Función para activar un modo STP en dispositivos 3Com y HPV1910 utilizando Paramiko.

    Parámetros:
        ip (number): Direccion IP del dispositivo.
        username (str): Usuario del dispositivo.
        password (str): Contrasena del dispositivo.
        region_name (str): Nombre de la region MSTP.
        modo (str): Modo de STP deseado (STP, RSTP o MSTP).
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
        conexion_ssh.send_command(channel, f"stp mode {modo}", wait_time=2)
        if modo == 'mstp':
            conexion_ssh.send_command(channel, "stp region-configuration", wait_time=2)
            conexion_ssh.send_command(channel, f"region-name {region_name}", wait_time=2)
            conexion_ssh.send_command(channel, "active region-configuration", wait_time=2)
        conexion_ssh.send_command(channel, "stp enable", wait_time=2)
        conexion_ssh.send_command(channel, "exit", wait_time=2)
        ssh.close()
        print("Configuración de STP completada con éxito.")
    except Exception as e:
        print(f"Error al configurar STP en {ip}: {e}")
        ssh.close()

def configurar_stpPriority_3com(ip, username, password, modo, prioridad, vlan, instance):
    """
    Función para configurar la prioridad STP en dispositivos 3Com y HPV1910 utilizando Paramiko.

    Parámetros:
        ip (number): Direccion IP del dispositivo.
        username (str): Usuario del dispositivo.
        password (str): Contrasena del dispositivo.
        prioridad (number): Numero de prioridad que va de 0 a 61440.
        modo (str): Modo de STP utilizado (STP, RSTP o MSTP).
        vlan (number): Numero de VLAN.
        instance (numero): Numero de instancia. 
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
        if modo == 'stp' or modo == 'rstp':
            conexion_ssh.send_command(channel, f"stp priority {prioridad}", wait_time=2)
        elif modo == 'pvst':
            conexion_ssh.send_command(channel, f"stp vlan {vlan} priority {prioridad}", wait_time=2)
        elif modo == 'mstp':
            conexion_ssh.send_command(channel, f"stp instance {instance} priority {prioridad}", wait_time=2)
        
        conexion_ssh.send_command(channel, "exit", wait_time=2)
        ssh.close()
        print("Configuración de STP completada con éxito.")
    except Exception as e:
        print(f"Error al configurar STP en {ip}: {e}")
        ssh.close()

#--------------------------------------------------------------------------------------------
#********************************* Configuracion TPLINK *************************************
#--------------------------------------------------------------------------------------------

def comandos_stp_tplink(region, modo):
    """
    Genera un archivo de texto con comandos de configuración para STP.

    Parámetros:
        region (str): Nombre de la región MSTP.
        modo (str): Modo de STP deseado (STP, RSTP o MSTP).
    """
    nombre_archivo = r'/home/paola/Documentos/loginapp/topologia/inventarios/comandos_stp.txt'
    
    if modo == 'mst':
        comandos = dedent(f"""
        configure
        spanning-tree mode {modo}
        spanning-tree extend system-id
        spanning-tree mst configuration
        name {region}
        exit
        """)
    else:
        comandos = dedent(f"""
        configure
        spanning-tree mode {modo}
        exit
        """)

    # Escribimos los comandos en el archivo
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(comandos.strip())

def comandos_stpPriority_tplink(prioridad):
    """
    Genera un archivo de texto con comandos de configuración para STP Priority.

    Parámetros:
        prioridad: Numero de prioridad que va de 0 a 61440.
    """
    nombre_archivo = r'/home/paola/Documentos/loginapp/topologia/inventarios/comandos_stp_prioridad.txt'
    # Preparar los comandos con los valores proporcionados
    
    comandos = dedent(f"""
        configure
        spanning-tree priority {prioridad}
        exit
    """)

    # Escribir los comandos en el archivo
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(comandos.strip())