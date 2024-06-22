import conexion_ssh
import config_vlan
import os
import read_yaml
import time



def procesar_dispositivos_vlan(datos_yaml):

    """
    Procesa una lista de dispositivos para crear VLANs según la información proporcionada en un archivo YAML.

    La función itera sobre cada grupo de dispositivos definido en el archivo YAML, extrae las configuraciones necesarias,
    y aplica las configuraciones correspondientes para crear VLANs utilizando diferentes bibliotecas y métodos según la marca y 
    características del dispositivo.

    Parámetros:
        datos_yaml (dict): Diccionario cargado desde un archivo YAML que contiene la información de configuración
                           para cada grupo de dispositivos.
    """

    if not datos_yaml:
        print("No se proporcionaron datos válidos.")
        return
    
    for grupo in datos_yaml:
        marca = datos_yaml[grupo]['vars']['marca']
        id_vlan= datos_yaml[grupo]['vars']['id']
        name_vlan= datos_yaml[grupo]['vars']['name_vlan']
        user = datos_yaml[grupo]['vars']['usuario']
        password = datos_yaml[grupo]['vars']['contrasena']
        device_type = datos_yaml[grupo]['vars']['device_type']
       

        for host, config in datos_yaml[grupo]['hosts'].items():
            ip = config['host']

            try:
                if marca in ['3COM', 'HPV1910']:  
                    # Usar Paramiko para dispositivos 3Com - HPV1910
                    config_vlan.configurar_vlan_3com(ip, user, password, id_vlan, name_vlan, save_config=True)

                elif marca == 'TPLINK':
                    archivo = config_vlan.comandos_vlan_tplink(id_vlan, name_vlan)
                    conexion_ssh.epmiko(user, password, ip, archivo)
                    print(f"VLAN {id_vlan} - '{name_vlan}' configurada exitosamente en el dispositivo {ip}.")


                else:
                    # Para Cisco y HPA5120, se utiliza Netmiko
                    dispositivo = {
                        'device_type': device_type,
                        'host': ip,
                        'username': user,
                        'password': password,
                    }
                    
                    connection = conexion_ssh.establecer_conexion_netmiko(dispositivo)

                    if connection:
                        if marca == 'CISCO':
                            config_vlan.configurar_vlan_cisco(connection, id_vlan, name_vlan, save_config=True)

                        elif marca == 'HPA5120':
                            config_vlan.configurar_vlan_hp(connection, id_vlan, name_vlan, save_config=True)
                        
                        connection.disconnect()
            except Exception as e:
                print(f"Error al configurar el dispositivo {ip}: {e}")

base_path = "/home/paola/Documentos/app2024/modulo_automatizacion/registros"
archivo = os.path.join(base_path, "datos_vlan.yaml")
datos_yaml = read_yaml.cargar_datos_snmp(archivo)
time_ini = time.time()
procesar_dispositivos_vlan(datos_yaml)
time_fin = time.time()
times = time_fin - time_ini
#print('El algoritmo de crear Vlans tardo: ', times)