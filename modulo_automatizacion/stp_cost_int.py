import conexion_ssh
import config_stp_cost
import os
import read_yaml

def procesar_dispositivos_stpCost(datos_yaml):

    """
    Procesa una lista de dispositivos para configurar el costo de una interfaz al emplear STP según la información proporcionada 
    en un archivo YAML.

    La función itera sobre cada grupo de dispositivos definido en el archivo YAML, extrae las configuraciones necesarias,
    y aplica las configuraciones STP correspondientes utilizando diferentes bibliotecas y métodos según la marca y 
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
        modo = datos_yaml[grupo]['vars']['modo']
        interfaz = datos_yaml[grupo]['vars']['interfaz']
        vlan = datos_yaml[grupo]['vars']['vlan']
        instance = datos_yaml[grupo]['vars']['instance']
        costo = datos_yaml[grupo]['vars']['costo']
        device_type = datos_yaml[grupo]['vars']['device_type']
        user = datos_yaml[grupo]['vars']['usuario']
        password = datos_yaml[grupo]['vars']['contrasena']
        

        for host, config in datos_yaml[grupo]['hosts'].items():
            ip = config['host']
            try: 
                if marca in ['3COM', 'HPV1910']:
                    # Usar Paramiko para dispositivos 3Com - HPV1910
                    config_stp_cost.configurar_stpCost_3com(ip, user, password, interfaz, modo, costo, vlan, instance)

                elif marca == 'TPLINK':
                    archivo = config_stp_cost.comandos_stpCost_tplink(interfaz, instance, costo)
                    conexion_ssh.epmiko(user, password, ip, archivo)
                    print(f"Configuración del costo {costo} en la interfaz {interfaz} completada con éxito.")

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
                            config_stp_cost.configurar_stpCost_cisco(connection, interfaz, costo)

                        elif marca == 'HPA5120':
                            config_stp_cost.configurar_stpCost_hp(connection, interfaz, modo, costo, vlan, instance)
                        connection.disconnect()
            except Exception as e:
                print(f"Error al configurar el dispositivo {ip}: {e}")

base_path = "/home/paola/Documentos/app2024/modulo_automatizacion/registros"
archivo = os.path.join(base_path, "datos_stpCost.yaml")
datos_yaml = read_yaml.cargar_datos_snmp(archivo)
procesar_dispositivos_stpCost(datos_yaml)