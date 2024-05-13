import conexion_ssh
import config_stp
import os
import read_yaml

def procesar_dispositivos_stpPriority(datos_yaml):
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
                    print(f"Configuracion STP-Prioridad EXITOSA en {ip} {marca}.")
                elif marca == 'TPLINK':
                    config_stp.comandos_stpPriority_tplink(prioridad)
                    conexion_ssh.epmiko(user)
                    print(f"Configuracion STP-Prioridad EXITOSA en {ip} {marca}.")
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
                            config_stp.configurar_stpPrioridad_cisco(connection, prioridad, vlan)
                            print(f"Configuracion STP-Prioridad EXITOSA en {ip} {marca}.")
                        elif marca == 'HPA5120':
                            config_stp.configurar_stpPrioridad_hp(connection, instance, modo, prioridad, vlan)
                            print(f"Configuracion STP-Prioridad EXITOSA en {ip} {marca}.")
                        connection.disconnect() 
            except Exception as e:
                print(f"Error al configurar el dispositivo {ip}: {e}")


base_path = "/home/paola/Documentos/loginapp/topologia/inventarios"
archivo = os.path.join(base_path, "datos_stpPriority.yaml")
datos_yaml = read_yaml.cargar_datos_snmp(archivo)
procesar_dispositivos_stpPriority(datos_yaml)