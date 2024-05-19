import paramiko
from textwrap import dedent
from conexion_ssh import send_command, interactive_send_command
import os

#--------------------------------------------------------------------------------------------
#********************************* Configuracion CISCO **************************************
#--------------------------------------------------------------------------------------------

def configurar_balanceo_cisco(connection, vlan_id, interfaz,save_config=False):

    commands = [
        f'vlan {vlan_id}',
        'exit',
        'spanning-tree mst configuration',
        f'instance 1 vlan {vlan_id}',
        'exit',
        f'int {interfaz}',
        'spanning-tree mst 1 cost 10',
    ]

    try:
        connection.send_config_set(commands)
        if save_config:
            connection.send_command('write memory')
        print(f"Configuración de balanceo de carga completada exitosamente")
    except Exception as e:
        print(f"Error al configurar balanceo de carga: {e}")



#--------------------------------------------------------------------------------------------
#****************************** Configuracion HPA5120 ***************************************
#--------------------------------------------connection, vlan_id, interfaz,save_config=False)----------------------------------------

def configurar_balanceo_hp(connection, vlan_id, interfaz,save_config=False):
    
    commands = [
        f'vlan {vlan_id}',
        'quit',
        'stp region-configuration',
        f'instance 1 vlan {vlan_id}',
        'quit',
        'stp pathcost-standard dot1d-1998',
        f'interface {interfaz}',
        f'stp instance 2 cost 10',
        'quit',
    ]

    try:
        connection.send_config_set(commands)
        if save_config:
            connection.send_command('save force')
        print(f"Configuración de balanceo de carga completada exitosamente.")
    except Exception as e:
        print(f"Error al configurar balanceo de carga: {e}")


#--------------------------------------------------------------------------------------------
#*******************************Configuracion 3COM y HPV1910 ********************************
#--------------------------------------------------------------------------------------------

def configurar_balanceo_3com(ip, username, password, vlan_id, interfaz, save_config=False):
   
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
        send_command(channel, f"vlan {vlan_id}", wait_time=2)
        send_command(channel, f"quit", wait_time=2)
        send_command(channel, f"stp region-configuration", wait_time=2)
        send_command(channel, f"instance 1 vlan {vlan_id}", wait_time=2)
        send_command(channel, f"quit", wait_time=2)
        send_command(channel, f"stp pathcost-standard dot1d-1998", wait_time=2)
        send_command(channel, f"interface {interfaz}", wait_time=2)
        send_command(channel, f"stp instance 2 cost 10", wait_time=2)
        send_command(channel, f"quit", wait_time=2)
        

        # Guardar la configuración si se indica
        if save_config:
            send_command(channel, "save", wait_time=2)
            interactive_send_command(channel, "Y", "Are you sure to overwrite the current configuration", "", wait_time=2)
        print("Configuración de balanceo de carga completada exitosamente.")
    except Exception as e:
        print(f"Error al configurar balanceo de carga: {e}")
    finally:
        ssh.close()



#--------------------------------------------------------------------------------------------
#********************************* Configuracion TPLINK *************************************
#--------------------------------------------------------------------------------------------

def comandos_balanceo_tplink (vlan_id, interfaz, archivo_destino=None):
    
    # Ruta predeterminada si no se especifica una
    if archivo_destino is None:
        archivo_destino = '/home/paola/Documentos/app2024/modulo_automatizacion/comandos/comandos_balanceo.txt'
    
    comandos = dedent(f"""
        configure
        vlan {vlan_id}
        exit
        spanning-tree mst configuration
        instance 2 vlan {vlan_id}
        exit
        interface {interfaz}
        spanning-tree mst instance 1 cost 10
        end
    """)

    # Aseguramos que el directorio donde se guardará el archivo exista
    os.makedirs(os.path.dirname(archivo_destino), exist_ok=True)

    # Escribimos los comandos en el archivo
    with open(archivo_destino, 'w') as archivo:
        archivo.write(comandos.strip())
    
    return archivo_destino
    