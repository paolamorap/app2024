import conexion_ssh
import config_logs
import os
import read_yaml

def procesar_dispositivos_logs(datos_yaml):

    """
    Procesa una lista de dispositivos para activar un servidor de LOGS según la información proporcionada en un archivo YAML.

    La función itera sobre cada grupo de dispositivos definido en el archivo YAML, extrae las configuraciones necesarias,
    y aplica las configuraciones de LOGS correspondientes utilizando diferentes bibliotecas y métodos según la marca y 
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
        servidorIP= datos_yaml[grupo]['vars']['servidorIP']
        trap= datos_yaml[grupo]['vars']['trap']
        user = datos_yaml[grupo]['vars']['usuario']
        password = datos_yaml[grupo]['vars']['contrasena']
        device_type = datos_yaml[grupo]['vars']['device_type']
       

        for host, config in datos_yaml[grupo]['hosts'].items():
            ip = config['host']
            
            try:
                if marca in ['3COM', 'HPV1910']:
                    # Usar Paramiko para dispositivos 3Com - HPV1910
                    config_logs.configurar_logs_3com(ip, user, password, servidorIP, save_config=True)

                elif marca == 'TPLINK':
                    archivo = config_logs.comandos_logs_tplink(servidorIP, trap)
                    conexion_ssh.epmiko(user, password, ip, archivo)
                    print(f"Configuración de logs completada exitosamente para el servidor {servidorIP}.")

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
                            config_logs.configurar_logs_cisco(connection, servidorIP, trap, save_config=True)

                        elif marca == 'HPA5120':
                            config_logs.configurar_logs_hp(connection, servidorIP, save_config=True)
                        connection.disconnect()
            except Exception as e:
                print(f"Error al configurar el dispositivo {ip}: {e}")

base_path = "/home/paola/Documentos/app2024/modulo_automatizacion/registros"
archivo = os.path.join(base_path, "datos_logs.yaml")
datos_yaml = read_yaml.cargar_datos_snmp(archivo)
procesar_dispositivos_logs(datos_yaml)
