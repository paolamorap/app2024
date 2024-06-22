import yaml
from netmiko import ConnectHandler
import paramiko
import time
import auto_comandos
import auto_tplink_comandos
import tplink_ssh_auto

#####################################################################
#----------------------#PROCESAR DISPOSITIVOS#-----------------------
#####################################################################

def cargar_configuracion_yaml(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        return yaml.safe_load(archivo)

def procesar_dispositivos(datos_yaml):
    for grupo in datos_yaml:
        user = datos_yaml[grupo]['vars']['epops_user']
        password = datos_yaml[grupo]['vars']['epops_ssh_pass']
        community = datos_yaml[grupo]['vars']['epops_snmp']
        device_type = datos_yaml[grupo]['vars']['device_type']
        marca = datos_yaml[grupo]['vars']['marca']

        for host, config in datos_yaml[grupo]['hosts'].items():
            ip = config['epops_host']
            print(f"Configurando SNMP en {ip} para el dispositivo de marca {marca}...")

            # Diferenciar entre dispositivos usando marca
            if marca == '3Com':
                # Usar Paramiko para dispositivos 3Com
                auto_comandos.configurar_snmp_3com(ip, user, password, community)
            elif marca == 'hp1':
                auto_comandos.configurar_snmp_3com(ip, user, password, community)
            elif marca == 'tplink':
                archivo = auto_tplink_comandos.comandos_snmp(community)
                tplink_ssh_auto.epmiko(user, password, ip, archivo)
            else:
                # Para Cisco y HP, se utiliza Netmiko
                dispositivo = {
                    'device_type': device_type,
                    'host': ip,
                    'username': user,
                    'password': password,
                    'secret': community,  # Opcional, si se necesita para entrar en modo enable
                }
                # Establecer conexión usando Netmiko
                connection = auto_comandos.establecer_conexion(dispositivo)
                if connection:
                    if marca == 'cisco':
                        auto_comandos.configurar_snmp_cisco(connection, community)
                    elif marca == 'hp':
                        auto_comandos.configurar_snmp_hp(connection, community)
                    # No olvides desconectar después de configurar
                    connection.disconnect()
                else:
                    print(f"No se pudo conectar al dispositivo {ip} con Netmiko.")