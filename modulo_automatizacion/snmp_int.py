import conexion_ssh
import config_snmp
import os
import read_yaml
import time

def procesar_dispositivos_snmp(datos_yaml):
    
    """
    Procesa una lista de dispositivos para configurar SNMP según la información proporcionada en un archivo YAML.

    La función itera sobre cada grupo de dispositivos definido en el archivo YAML, extrae las configuraciones necesarias,
    y aplica las configuraciones SNMP correspondientes utilizando diferentes bibliotecas y métodos según la marca y 
    características del dispositivo.

    Parámetros:
        datos_yaml (dict): Diccionario cargado desde un archivo YAML que contiene la información de configuración
                           para cada grupo de dispositivos.
    """

    if not datos_yaml:
        print("No se proporcionaron datos válidos.")
        return

    for grupo in datos_yaml:
        marca = datos_yaml[grupo]['vars'].get('marca')
        community = datos_yaml[grupo]['vars'].get('comunidad')
        permiso = datos_yaml[grupo]['vars'].get('permisos')
        id_list = datos_yaml[grupo]['vars'].get('id_list')
        user = datos_yaml[grupo]['vars'].get('usuario')
        password = datos_yaml[grupo]['vars'].get('contrasena')
        device_type = datos_yaml[grupo]['vars'].get('device_type')

        for host, config in datos_yaml[grupo]['hosts'].items():
            ip = config['host']
            try:
                # Configuración SNMP específica por marca y modelo de dispositivo
                if marca in ['3COM', 'HPV1910']:  
                    # Configuración para dispositivos 3Com - HPV1910 usando Paramiko
                    if id_list == "SN":
                        config_snmp.configurar_snmp_3com(ip, user, password, community, permiso, save_config=True)
                    else:
                        config_snmp.configurar_snmp_acl_3com(ip, user, password, community, permiso, id_list, save_config=True)
                    
                elif marca == 'TPLINK':
                    # Configuración para dispositivos TPLINK usando un script SSH
                    archivo = config_snmp.comandos_snmp_tplink(community, permiso)
                    conexion_ssh.epmiko(user, password, ip, archivo)
                    print(f"Configuración SNMP con comunidad '{community}' y permiso '{permiso}' completada exitosamente.")

                else:
                    # Configuración para dispositivos Cisco y HPA5120 usando Netmiko
                    dispositivo = {
                        'device_type': device_type,
                        'host': ip,
                        'username': user,
                        'password': password,
                    }

                    connection = conexion_ssh.establecer_conexion_netmiko(dispositivo)
                    
                    if connection:
                        if marca == 'CISCO':
                            if id_list == "SN":
                                config_snmp.configurar_snmp_cisco(connection, community, permiso, save_config=True)
                            else:
                                config_snmp.configurar_snmp_acl_cisco(connection, community, permiso, id_list, save_config=True)
                        elif marca == 'HPA5120':
                            if id_list == "SN":
                                config_snmp.configurar_snmp_hp(connection, community, permiso, save_config=True)
                            else:
                                config_snmp.configurar_snmp_acl_hp(connection, community, permiso, id_list, save_config=True)
                        connection.disconnect()
            except Exception as e:
                print(f"Error al configurar el dispositivo {ip}: {e}")

# Uso del código
base_path = "/home/paola/Documentos/app2024/modulo_automatizacion/registros"
archivo = os.path.join(base_path, "datos_snmp.yaml")
time_ini = time.time()
datos_yaml = read_yaml.cargar_datos_snmp(archivo)
procesar_dispositivos_snmp(datos_yaml)
time_fin = time.time()
times = time_fin - time_ini
print('El algoritmo de crear una comunidad SNMP tardo: ', times)
