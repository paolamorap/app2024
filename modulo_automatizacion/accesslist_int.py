import conexion_ssh
import config_acl
import os
import read_yaml
import time

def procesar_dispositivos_accesslist(datos_yaml):
    
    """
    Procesa una lista de dispositivos para configurar una ACCESS LIST según la información proporcionada en un archivo YAML.

    La función itera sobre cada grupo de dispositivos definido en el archivo YAML, extrae las configuraciones necesarias,
    y aplica las configuraciones de access list correspondientes utilizando diferentes bibliotecas y métodos según la marca y 
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
        ip_red= datos_yaml[grupo]['vars']['ip_red']
        mascara_wildcard= datos_yaml[grupo]['vars']['mascara_wildcard']
        id_list= datos_yaml[grupo]['vars']['id_list']
        n_rule= datos_yaml[grupo]['vars']['n_rule']
        user = datos_yaml[grupo]['vars']['usuario']
        password = datos_yaml[grupo]['vars']['contrasena']
        device_type = datos_yaml[grupo]['vars']['device_type']
       

        for host, config in datos_yaml[grupo]['hosts'].items():
            ip = config['host']
            
            try:
                if marca in ['3COM', 'HPV1910']:
                    # Usar Paramiko para dispositivos 3Com - HPV1910
                    config_acl.configurar_acl_3com(ip, user, password, n_rule, id_list, ip_red, mascara_wildcard, save_config=True)

                elif marca == 'TPLINK':
                    archivo = config_acl.comandos_acl_tplink(n_rule, id_list, ip_red, mascara_wildcard)
                    conexion_ssh.epmiko(user, password, ip, archivo)
                    print(f"Access List {id_list} creada con éxito en la red {ip_red}.")

                else:
                    # Para Cisco y HPv1910, se utiliza Netmiko
                    dispositivo = {
                        'device_type': device_type,
                        'host': ip,
                        'username': user,
                        'password': password,
                    }
                    
                    connection = conexion_ssh.establecer_conexion_netmiko(dispositivo)

                    if connection:
                        if marca == 'CISCO':
                            config_acl.configurar_acl_cisco(connection, id_list, ip_red, mascara_wildcard, save_config=True)

                        elif marca == 'HPA5120':
                            config_acl.configurar_acl_hp(connection, n_rule, id_list, ip_red, mascara_wildcard, save_config=True)
                            
                        connection.disconnect()
            except Exception as e:
                print(f"Error al configurar el dispositivo {ip}: {e}")

base_path = "/home/paola/Documentos/app2024/modulo_automatizacion/registros"
archivo = os.path.join(base_path, "datos_access_list.yaml")
datos_yaml = read_yaml.cargar_datos_snmp(archivo)
time_ini = time.time()
procesar_dispositivos_accesslist(datos_yaml)
time_fin = time.time()
times = time_fin - time_ini
print('El algoritmo de configurar lista de acceso tardo: ', times)
