import conexion_ssh
import config_vlan
import os
import read_yaml


def procesar_dispositivos_vlan(datos_yaml):
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
                    config_vlan.configurar_vlan_3com(ip, user, password, id_vlan, name_vlan)
                    print(f"VLAN {id_vlan} creada EXITOSAMENTE en {ip} {marca}.")

                elif marca == 'TPLINK':
                    config_vlan.comandos_vlan_tplink(id_vlan, name_vlan)
                    conexion_ssh.epmiko(user)
                    print(f"VLAN {id_vlan} creada EXITOSAMENTE en {ip} {marca}.")

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
                            config_vlan.configurar_vlan_cisco(connection, id_vlan, name_vlan)
                            print(f"VLAN {id_vlan} creada EXITOSAMENTE en {ip} {marca}.")

                        elif marca == 'HPA5120':
                            config_vlan.configurar_vlan_hp(connection, id_vlan, name_vlan)
                            print(f"VLAN {id_vlan} creada EXITOSAMENTE en {ip} {marca}.")
                        
                        connection.disconnect()
            except Exception as e:
                print(f"Error al configurar el dispositivo {ip}: {e}")

base_path = "/home/paola/Documentos/loginapp/topologia/inventarios"
archivo = os.path.join(base_path, "datos_vlan.yaml")
datos_yaml = read_yaml.cargar_datos_snmp(archivo)
procesar_dispositivos_vlan(datos_yaml)