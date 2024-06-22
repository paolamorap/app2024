import conexion_ssh
import config_balanceo
import os
import read_yaml

def procesar_dispositivos_balanceo(datos_yaml):
    
    """
    Procesa una lista de dispositivos para configurar el BALANCEO DE CARGA según la información proporcionada en un archivo YAML.
    Parámetros:
        datos_yaml (dict): Diccionario cargado desde un archivo YAML que contiene la información de configuración
                           para cada grupo de dispositivos.
    """

    if not datos_yaml:
        print("No se proporcionaron datos válidos.")
        return

    for grupo in datos_yaml:
        modo = datos_yaml[grupo]['vars'].get('modoSTP')
        vlan= datos_yaml[grupo]['vars'].get('vlan1')
        user = datos_yaml[grupo]['vars'].get('user')
        password = datos_yaml[grupo]['vars'].get('password')
        

        for host, config in datos_yaml[grupo]['enlace'].items():
            
            ip = config['IP']
            #print(ip)
            interfaz = config['interfaz1']
            #print(interfaz)
            marca = config['marca']

            if marca == 'CISCO':
                device = 'cisco_ios'
            elif marca == 'HPV1910':
                device = 'hp_comware'
            else:
                device='none'

            device_type = device
            #print(marca)
            #print(device_type)

            try:
                # Configuración SNMP específica por marca y modelo de dispositivo
                if marca in ['3COM', 'HPV1910']:  
                    config_balanceo.configurar_balanceo_3com(ip, user, password, vlan, interfaz, save_config=False)

                elif marca == 'TPLINK':
                    archivo = config_balanceo.comandos_balanceo_tplink(vlan, interfaz)
                    conexion_ssh.epmiko(user, password, ip, archivo)
                    print(f"Configuración de balanceo de carga completada exitosamente.")

                else:
                    # Configuración para dispositivos Cisco y HPA5120 usando Netmiko
                    dispositivo = {
                        'device_type': device_type,
                        'host': ip,
                        'username': user,
                        'password': password,
                        'timeout':60,
                        'session_log': 'log.txt'
                    }

                    connection = conexion_ssh.establecer_conexion_netmiko(dispositivo)
                    
                    if connection:
                        if marca == 'CISCO':
                            config_balanceo.configurar_balanceo_cisco(connection, vlan, interfaz, save_config=False)
                        elif marca == 'HPA5120':
                            config_balanceo.configurar_balanceo_hp(connection, vlan, interfaz, save_config=False)
                        connection.disconnect()
            except Exception as e:
                print(f"Error al configurar el dispositivo {ip}: {e}")

# Uso del código
base_path = "/home/paola/Documentos/app2024/modulo_automatizacion/registros"
archivo = os.path.join(base_path, "datos_balanceo.yaml")
datos_yaml = read_yaml.cargar_datos_snmp(archivo)
procesar_dispositivos_balanceo(datos_yaml)
