import conexion_ssh
import config_stp
import os
import read_yaml
import time

def procesar_dispositivos_stpPriority(datos_yaml):
    
    """
    Procesa una lista de dispositivos para configurar la priorirdad STP según la información proporcionada en un archivo YAML.

    La función itera sobre cada grupo de dispositivos definido en el archivo YAML, extrae las configuraciones necesarias,
    y aplica las configuraciones STP Priority correspondientes utilizando diferentes bibliotecas y métodos según la marca y 
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
        prioridad = datos_yaml[grupo]['vars']['prioridad']
        vlan = datos_yaml[grupo]['vars']['vlan']
        modo = datos_yaml[grupo]['vars']['modo']
        instance = datos_yaml[grupo]['vars']['instance']
        device_type = datos_yaml[grupo]['vars']['device_type']
        user = datos_yaml[grupo]['vars']['usuario']
        password = datos_yaml[grupo]['vars']['contrasena']
        
        for host, config in datos_yaml[grupo]['hosts'].items():
            ip = config['host']

            try: 
                if marca in ['3COM', 'HPV1910']:
                    # Usar Paramiko para dispositivos 3Com - HPV19210
                    config_stp.configurar_stpPriority_3com (ip, user, password, modo, prioridad, vlan, instance)

                elif marca == 'TPLINK':
                    archivo = config_stp.comandos_stpPriority_tplink(prioridad)
                    conexion_ssh.epmiko(user, password, ip, archivo)
                    print("Configuración de prioridad STP completada con éxito.")

                else:
                    # Para Cisco y HP, se utiliza Netmiko
                    dispositivo = {
                        'device_type': device_type,
                        'host': ip,
                        'username': user,
                        'password': password,
                    }
                    # Establecer conexión usando Netmiko
                    connection = conexion_ssh.establecer_conexion_netmiko(dispositivo)
                    if connection:
                        if marca == 'CISCO':
                            config_stp.configurar_stpPrioridad_cisco(connection, prioridad, instance, vlan, modo)
                        elif marca == 'HPA5120':
                            config_stp.configurar_stpPrioridad_hp(connection, instance, modo, prioridad, vlan)
                        connection.disconnect() 
            except Exception as e:
                print(f"Error al configurar el dispositivo {ip}: {e}")


base_path = "/home/paola/Documentos/app2024/modulo_automatizacion/registros"
archivo = os.path.join(base_path, "datos_stpPriority.yaml")
datos_yaml = read_yaml.cargar_datos_snmp(archivo)
time_ini = time.time()
procesar_dispositivos_stpPriority(datos_yaml)
time_fin = time.time()
times = time_fin - time_ini
print('El algoritmo de configurar STP Prioridad tardo: ', times)