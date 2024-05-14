import paramiko
from textwrap import dedent
from conexion_ssh import send_command, interactive_send_command
import os


#--------------------------------------------------------------------------------------------
#********************************* Configuracion CISCO **************************************
#--------------------------------------------------------------------------------------------

def configurar_stpMode_cisco(connection, modo, region_name):
    """
    Configura el modo Spanning Tree Protocol (STP) en dispositivos Cisco utilizando Netmiko.

    Esta función establece el modo de operación del STP en dispositivos Cisco, permitiendo seleccionar entre PVST, Rapid-PVST y MST.
    Para el modo MST, también permite configurar un nombre de región.

    Parámetros:
        connection (Netmiko Connection): Conexión activa al dispositivo Cisco.
        modo (str): Modo de STP deseado ('pvst', 'rapid-pvst', 'mst').
        region_name (str, opcional): Nombre de la región para configuraciones MST. Requerido si el modo es 'mst'.

    """
    commands = [
        f'spanning-tree mode {modo}'
    ]
    
    if modo == 'mst':
        if region_name is None:
            raise ValueError("El nombre de la región es necesario para el modo MST")
        commands.extend([
            'spanning-tree mst configuration',
            f'name {region_name}',
        ])
        
    commands.append('end')
    commands.append('wr')
    
    try:
        connection.send_config_set(commands)
        print(f"Configuración de STP en modo {modo} completada con éxito.")
    except Exception as e:
        print(f"Error al configurar STP en modo {modo}: {e}")


def configurar_stpPrioridad_cisco(connection, prioridad, instanceID, vlanID, modo):
    """
    Configura la prioridad del Spanning Tree Protocol (STP) para una VLAN específica en dispositivos Cisco utilizando Netmiko.

    Esta función establece la prioridad de STP para una VLAN determinada, lo cual es crucial en la configuración del algoritmo
    de Spanning Tree para influir en la selección del puente raíz en una red segmentada por VLANs.

    Parámetros:
        connection (Netmiko Connection): Conexión activa al dispositivo Cisco.
        prioridad (int): Número de prioridad que se debe establecer para la VLAN, en el rango de 0 a 61440.
        vlanID (int): Identificador de la VLAN para la que se está configurando la prioridad.

    """
    commands = []

    if modo == 'pvst' or modo == 'rapid-pvst':
        commands.append(f'spanning-tree vlan {vlanID} priority {prioridad}')
    elif modo == 'mst':
        commands.append(f'spanning-tree mst {instanceID} priority {prioridad}')

    commands.append('end')
    commands.append('wr')
    
    
    try:
        connection.send_config_set(commands)
        print(f"Configuración de prioridad STP para modo {modo} completada con éxito.")
    except Exception as e:
        print(f"Error al configurar prioridad STP: {e}")


#--------------------------------------------------------------------------------------------
#****************************** Configuracion HPA5120 ***************************************
#--------------------------------------------------------------------------------------------

def configurar_stpMode_hp(connection, region_name, modo):
    """
    Configura el modo Spanning Tree Protocol (STP) en dispositivos HPA5120 utilizando Netmiko.

    Esta función activa y configura el modo STP deseado en el dispositivo, soportando configuraciones para STP, RSTP, y MSTP.
    En el caso de MSTP, permite también definir una configuración de región, que es aplicada y activada.

    Parámetros:
        connection (Netmiko Connection): Conexión activa al dispositivo HP.
        region_name (str): Nombre de la región MST, utilizado solo si el modo es MSTP.
        modo (str): Modo de STP deseado ('stp', 'rstp', 'mstp').
        save_config (bool): Si es True, guarda la configuración en la memoria permanente del dispositivo.

    """
    commands = [
        f'stp mode {modo}'
    ]
    
    if modo == 'mstp':
        # Configuración específica para MSTP
        commands.extend([
            'stp region-configuration',
            f'region-name {region_name}',
            'active region-configuration',
        ])
    commands.append('quit')
    try:
        connection.send_config_set(commands)
        print(f"Configuración de STP en modo {modo} completada con éxito.")
    except Exception as e:
        print(f"Error al configurar STP en modo {modo}: {e}")


def configurar_stpPrioridad_hp(connection, instance, modo, prioridad, vlan):
    """
    Configura la prioridad del protocolo Spanning Tree (STP) en dispositivos HPA5120 utilizando Netmiko.

    Esta función permite configurar la prioridad STP en diferentes modos (STP, RSTP, PVST, MSTP) dependiendo de las necesidades
    del entorno de red. Permite una gran flexibilidad en la gestión del tráfico y la prevención de bucles de red.

    Parámetros:
        connection (Netmiko Connection): Conexión activa al dispositivo HP.
        instance (int): Número de instancia para MSTP. Por defecto es 0, agrupando todas las VLANs que no están asignadas a otra instancia.
        modo (str): Modo de STP utilizado ('stp', 'rstp', 'pvst', 'mstp').
        prioridad (int): Prioridad de STP, valor entre 0 y 61440.
        vlan (str): Especificación de VLAN o rango de VLANs, aplicable solo en modos PVST y MSTP.
        save_config (bool): Si es True, guarda la configuración en la memoria permanente del dispositivo.

    """
    commands = []
    
    if modo == 'stp' or modo == 'rstp':
        commands.append(f'stp priority {prioridad}')
    elif modo == 'pvst':
        commands.append(f'stp vlan {vlan} priority {prioridad}')
    elif modo == 'mstp':
        commands.append(f'stp instance {instance} priority {prioridad}')

    commands.append('quit')

    try:
        connection.send_config_set(commands)
        print(f"Configuración de prioridad STP para modo {modo} completada con éxito.")
    except Exception as e:
        print(f"Error al configurar prioridad STP: {e}")


#--------------------------------------------------------------------------------------------
#*******************************Configuracion 3COM y HPV1910 ********************************
#--------------------------------------------------------------------------------------------

def configurar_STP_3com(ip, username, password, region_name, modo):
    """
    Configura el protocolo de árbol de expansión (Spanning Tree Protocol, STP) en dispositivos 3Com y HPV1910 
    utilizando Paramiko para establecer una conexión SSH.

    Esta función activa y configura el modo STP deseado en el dispositivo, permitiendo la configuración de STP, RSTP, o MSTP
    dependiendo de los parámetros suministrados. También permite la configuración de una región MSTP si se selecciona dicho modo.

    Parámetros:
        ip (str): Dirección IP del dispositivo.
        username (str): Usuario del dispositivo.
        password (str): Contraseña del dispositivo.
        region_name (str): Nombre de la región MSTP, utilizado sólo si el modo es 'mstp'.
        modo (str): Modo de STP deseado ('stp', 'rstp', o 'mstp').
        save_config (bool): Si es True, guarda la configuración en la memoria permanente del dispositivo.

    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password)  
        channel = ssh.invoke_shell()
        send_command(channel, "_cmdline-mode on", wait_time=2)
        interactive_send_command(
            channel,
            "Y",  # Confirmación para entrar en el modo de línea de comandos.
            "Please input password:",  # Mensaje esperado antes de enviar la contraseña.
            "512900",  # Contraseña para el modo de línea de comandos.
            wait_time=2
        )
        send_command(channel, "system-view", wait_time=2)
        send_command(channel, f"stp mode {modo}", wait_time=2)

        if modo == 'mstp':
            send_command(channel, "stp region-configuration", wait_time=2)
            send_command(channel, f"region-name {region_name}", wait_time=2)
            send_command(channel, "active region-configuration", wait_time=2)

        send_command(channel, f"quit", wait_time=2)
        print(f"Configuración de STP en modo {modo} completada con éxito.")
    except Exception as e:
        print(f"Error al configurar STP en modo {modo}: {e}")
    finally:
        ssh.close()
        

def configurar_stpPriority_3com(ip, username, password, modo, prioridad, vlan, instance):
    """
    Configura la prioridad STP en dispositivos 3Com y HPV1910 para diferentes modos y escenarios utilizando Paramiko.

    Esta función establece la prioridad de Spanning Tree Protocol (STP) en dispositivos 3Com y HPV1910, ajustando los valores
    según el modo y contexto específico (STP, RSTP, MSTP o PSTP para cisco).

    Parámetros:
        ip (str): Dirección IP del dispositivo.
        username (str): Usuario del dispositivo.
        password (str): Contraseña del dispositivo.
        modo (str): Modo de STP utilizado ('stp', 'rstp', 'pvst', 'mstp').
        prioridad (int): Prioridad de STP, valor entre 0 y 61440.
        vlan (int): Número de VLAN, relevante solo para 'pvst'.
        instance (int): Número de instancia, relevante solo para 'mstp'.
        save_config (bool): Si es True, guarda la configuración en la memoria permanente del dispositivo.

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
            wait_time=2
        )
        send_command(channel, "system-view", wait_time=2)
        if modo in ['stp', 'rstp']:
            send_command(channel, f"stp priority {prioridad}", wait_time=2)
        elif modo == 'pvst':
            send_command(channel, f"stp vlan {vlan} priority {prioridad}", wait_time=2)
        elif modo == 'mstp':
            send_command(channel, f"stp instance {instance} priority {prioridad}", wait_time=2)

        send_command(channel, f"quit", wait_time=2)
        print(f"Configuración de prioridad STP para modo {modo} completada con éxito.")
    except Exception as e:
        print(f"Error al configurar prioridad STP: {e}")
    finally:
        ssh.close()
#--------------------------------------------------------------------------------------------
#********************************* Configuracion TPLINK *************************************
#--------------------------------------------------------------------------------------------

def comandos_stp_tplink(region, modo, archivo_destino=None):
    """
    Genera un archivo de texto con comandos de configuración para el protocolo Spanning Tree (STP) en dispositivos TP-Link.

    Esta función crea comandos de configuración STP, adecuados para distintos modos, incluyendo configuraciones especiales
    para MSTP que incluyen la definición de una región.

    Parámetros:
        region (str): Nombre de la región MSTP, necesario solo si el modo es MSTP.
        modo (str): Modo de STP deseado ('STP', 'RSTP', o 'MSTP').
        archivo_destino (str, opcional): Ruta completa del archivo donde se guardarán los comandos. Si no se proporciona, se 
        usa una ruta predeterminada.

    Retorna:
        str: Ruta al archivo generado con los comandos.
    """

    # Ruta predeterminada si no se especifica una
    if archivo_destino is None:
        archivo_destino = '/home/paola/Documentos/app2024/modulo_automatizacion/comandos/comandos_stp.txt'
    
    comandos = dedent(f"""
        configure
        spanning-tree mode {modo}
        """)

    if modo == 'mst':
        comandos += dedent(f"""
        spanning-tree extend system-id
        spanning-tree mst configuration
        name {region}
        end
        """)
    else:
        comandos += "end\n"

    # Aseguramos que el directorio donde se guardará el archivo exista
    os.makedirs(os.path.dirname(archivo_destino), exist_ok=True)

    # Escribimos los comandos en el archivo
    with open(archivo_destino, 'w') as archivo:
        archivo.write(comandos.strip())
    
    return archivo_destino


def comandos_stpPriority_tplink(prioridad, archivo_destino=None):
    """
    Genera un archivo de texto con comandos para configurar la prioridad del protocolo Spanning Tree (STP) en dispositivos 
    TP-Link.

    Esta función crea comandos para ajustar la prioridad del STP, lo cual es crucial para la selección del puente raíz en redes 
    segmentadas.

    Parámetros:
        prioridad (int): Número de prioridad para STP, en el rango de 0 a 61440.
        archivo_destino (str, opcional): Ruta completa del archivo donde se guardarán los comandos. Si no se proporciona, se usa 
        una ruta predeterminada.

    Retorna:
        str: Ruta al archivo generado con los comandos.
    """

    # Ruta predeterminada si no se especifica una
    if archivo_destino is None:
        archivo_destino = '/home/paola/Documentos/app2024/modulo_automatizacion/comandos/comandos_stp_prioridad.txt'

    comandos = dedent(f"""
        configure
        spanning-tree priority {prioridad}
        exit
    """)

    # Aseguramos que el directorio donde se guardará el archivo exista
    os.makedirs(os.path.dirname(archivo_destino), exist_ok=True)

    # Escribimos los comandos en el archivo
    with open(archivo_destino, 'w') as archivo:
        archivo.write(comandos.strip())
    
    return archivo_destino
