import paramiko
from textwrap import dedent
from conexion_ssh import send_command, interactive_send_command
import os


#--------------------------------------------------------------------------------------------
#********************************* Configuracion CISCO **************************************
#--------------------------------------------------------------------------------------------


def configurar_stpCost_cisco(connection, interfaz, costo):
    """
    Configura el costo por interfaz del Spanning Tree Protocol (STP) en dispositivos Cisco utilizando Netmiko.

    Esta función establece un costo a una interfaz donde corre STP en cualquier modo, lo cual es esencial en la configuración del algoritmo
    de Spanning Tree para influir en la selección del puente raíz en una red. Ajustar el costo puede ayudar a optimizar la topología de la
    red y mejorar la resiliencia del tráfico.

    Parámetros:
        connection (Netmiko Connection): Conexión activa al dispositivo Cisco.
        interfaz (str): Nombre de la interfaz en la que se va a configurar el costo del STP (por ejemplo, 'GigabitEthernet0/1').
        costo (int): Costo del STP que se debe establecer para la interfaz. El valor del costo debe estar en el rango adecuado 
        para el dispositivo y la configuración de red.
    """
    commands = [
        f"interface {interfaz}",
        f"spanning-tree cost {costo}",
        'end',
        'wr',
    ]
    
    try:
        connection.send_config_set(commands)
        print(f"Configuración del costo {costo} en la interfaz {interfaz} completada con éxito.")
    except Exception as e:
        print(f"Error al configurar pathcost STP: {e}")


#--------------------------------------------------------------------------------------------
#****************************** Configuracion HPA5120 ***************************************
#--------------------------------------------------------------------------------------------

def configurar_stpCost_hp(connection, interfaz, modo, costo, vlan=None, instance=None):
    """
    Configura el costo por interfaz del Spanning Tree Protocol (STP) en dispositivos HP A5120 utilizando Netmiko.

    Esta función establece un costo a una interfaz según el modo de STP seleccionado (STP, RSTP, PVST, MSTP). 
    Es esencial en la configuración del algoritmo de Spanning Tree para influir en la selección del puente raíz 
    en una red. Ajustar el costo puede ayudar a optimizar la topología de la red y mejorar la resiliencia del tráfico.

    Parámetros:
        connection (Netmiko Connection): Conexión activa al dispositivo HP.
        interfaz (str): Nombre de la interfaz en la que se va a configurar el costo del STP (por ejemplo, 'GigabitEthernet0/1').
        modo (str): Modo de STP empleado en la red ('stp', 'rstp', 'pvst', 'mstp').
        costo (int): Costo del STP que se debe establecer para la interfaz. El valor del costo debe estar en el rango adecuado 
        para el dispositivo y la configuración de red.
        vlan (int, opcional): Identificador de la VLAN, utilizado solo si el modo es PVST.
        instance (int, opcional): Número de instancia MST, utilizado solo si el modo es MSTP.

    """
    commands = [
        f'interface {interfaz}'
    ]
    
    if modo == 'stp' or modo == 'rstp':
        commands.append(f'stp cost {costo}')
    elif modo == 'pvst':
        if vlan is not None:
            commands.append(f'stp vlan {vlan} cost {costo}')
        else:
            raise ValueError("El parámetro 'vlan' es requerido cuando el modo es 'pvst'.")
    elif modo == 'mstp':
        if instance is not None:
            commands.append(f'stp instance {instance} cost {costo}')
        else:
            raise ValueError("El parámetro 'instance' es requerido cuando el modo es 'mstp'.")

    commands.append('quit')
    
    try:
        connection.send_config_set(commands)
        print(f"Configuración del costo {costo} en la interfaz {interfaz} completada con éxito.")
    except Exception as e:
        print(f"Error al configurar pathcost STP: {e}")

#--------------------------------------------------------------------------------------------
#*******************************Configuracion 3COM y HPV1910 ********************************
#--------------------------------------------------------------------------------------------

def configurar_stpCost_3com(ip, username, password, interfaz, modo, costo, vlan=None, instance=None):
    """
    Configura el costo por interfaz del Spanning Tree Protocol (STP) en dispositivos 3Com y HP V1910 utilizando Paramiko.

    Esta función establece un costo a una interfaz según el modo de STP seleccionado (STP, RSTP, PVST, MSTP). 
    Es esencial en la configuración del algoritmo de Spanning Tree para influir en la selección del puente raíz 
    en una red. Ajustar el costo puede ayudar a optimizar la topología de la red y mejorar la resiliencia del tráfico.

    Parámetros:
        ip (str): Dirección IP del dispositivo.
        username (str): Nombre de usuario para la autenticación en el dispositivo.
        password (str): Contraseña para la autenticación en el dispositivo.
        interfaz (str): Nombre de la interfaz en la que se va a configurar el costo del STP (por ejemplo, 'GigabitEthernet0/1').
        modo (str): Modo de STP empleado en la red ('stp', 'rstp', 'pvst', 'mstp').
        costo (int): Costo del STP que se debe establecer para la interfaz. El valor del costo debe estar en el rango adecuado 
                     para el dispositivo y la configuración de red.
        vlan (int, opcional): Identificador de la VLAN, utilizado solo si el modo es PVST.
        instance (int, opcional): Número de instancia MST, utilizado solo si el modo es MSTP.

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
        send_command(channel, f"interface {interfaz}", wait_time=2)

        if modo in ['stp', 'rstp']:
            send_command(channel, f"stp cost {costo}", wait_time=2)
        elif modo == 'pvst':
            send_command(channel, f"stp vlan {vlan} cost {costo}", wait_time=2)
        elif modo == 'mstp':
            send_command(channel, f"stp instance {instance} cost {costo}", wait_time=2)

        send_command(channel, "quit", wait_time=2)

        print(f"Configuración del costo {costo} en la interfaz {interfaz} completada con éxito.")
    except Exception as e:
        print(f"Error al configurar pathcost STP: {e}")
    finally:
        ssh.close()

#--------------------------------------------------------------------------------------------
#********************************* Configuracion TPLINK *************************************
#--------------------------------------------------------------------------------------------


import os
from textwrap import dedent

def comandos_stpCost_tplink(interfaz, instance, cost, archivo_destino=None):
    """
    Genera un archivo de texto con comandos para configurar el costo por interfaz del Spanning Tree Protocol (STP) 
    en dispositivos TP-Link.

    Parámetros:
        interfaz (str): Nombre de la interfaz en la que se va a configurar el costo del STP (por ejemplo, 'GigabitEthernet0/1').
        instance (int): Número de instancia MST en la que se va a configurar el costo.
        cost (int): Costo del STP que se debe establecer para la interfaz.
        archivo_destino (str, opcional): Ruta completa del archivo donde se guardarán los comandos. 
                                         Si no se proporciona, se usa una ruta predeterminada.

    Retorna:
        str: Ruta al archivo generado con los comandos.
    """

    # Ruta predeterminada si no se especifica una
    if archivo_destino is None:
        archivo_destino = '/home/paola/Documentos/app2024/modulo_automatizacion/comandos/comandos_stp_cost.txt'

    comandos = dedent(f"""
        configure
        interface {interfaz}              
        spanning-tree mst instance {instance} cost {cost}
        exit
    """)

    # Aseguramos que el directorio donde se guardará el archivo exista
    os.makedirs(os.path.dirname(archivo_destino), exist_ok=True)

    # Escribimos los comandos en el archivo
    with open(archivo_destino, 'w') as archivo:
        archivo.write(comandos.strip())
    
    return archivo_destino

