import conexion_ssh
import config_stp
import os
import read_yaml

def procesar_dispositivos_stpActive(datos_yaml):
    if not datos_yaml:
        print("No se proporcionaron datos válidos.")
        return
    
    for grupo in datos_yaml:
        marca = datos_yaml[grupo]['vars']['marca']
        region = datos_yaml[grupo]['vars']['region']
        modo = datos_yaml[grupo]['vars']['modo']
        device_type = datos_yaml[grupo]['vars']['device_type']
        user = datos_yaml[grupo]['vars']['usuario']
        password = datos_yaml[grupo]['vars']['contrasena']
        

        for host, config in datos_yaml[grupo]['hosts'].items():
            ip = config['host']
            try: 
                if marca in ['3COM', 'HPV1910']:
                    # Usar Paramiko para dispositivos 3Com - HPV1910
                    config_stp.configurar_STP_3com(ip, user, password, modo, region)
                    print(f"STP {modo} ACTIVADO EXITOSAMENTE EN {ip} {marca}.")

                elif marca == 'TPLINK':
                    config_stp.comandos_stp_tplink(modo, region)
                    conexion_ssh.epmiko(user)
                    print(f"STP {modo} ACTIVADO EXITOSAMENTE EN {ip} {marca}.")

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
                            config_stp.configurar_stpMode_cisco(connection, region, modo)
                            print(f"STP {modo} ACTIVADO EXITOSAMENTE EN {ip} {marca}.")

                        elif marca == 'HPA5120':
                            config_stp.configurar_stpMode_hp(connection, region, modo)
                            print(f"STP {modo} ACTIVADO EXITOSAMENTE EN {ip} {marca}.")
                        connection.disconnect()
            except Exception as e:
                print(f"Error al configurar el dispositivo {ip}: {e}")

base_path = "/home/paola/Documentos/loginapp/topologia/inventarios"
archivo = os.path.join(base_path, "datos_stp.yaml")
datos_yaml = read_yaml.cargar_datos_snmp(archivo)
procesar_dispositivos_stpActive(datos_yaml)
