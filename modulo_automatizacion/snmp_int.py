import conexion_ssh
import config_snmp
import os
import read_yaml

def procesar_dispositivos_snmp(datos_yaml):
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
                if marca in ['3COM', 'HPV1910']:  
                    # Usar Paramiko para dispositivos 3Com - HPV1910
                    if id_list == "SN":
                        config_snmp.configurar_snmp_3com(ip, user, password, community, permiso)
                        print(f"Configuracion SNMP EXITOSA en {ip} {marca}.")
                    else:
                        config_snmp.configurar_snmp_acl_3com(ip, user, password, community, permiso, id_list)
                        print(f"Configuracion SNMP EXITOSA en {ip} {marca} con {id_list} como lista de acceso.")
                    
                elif marca == 'TPLINK':
                    config_snmp.comandos_snmp(community, permiso)
                    conexion_ssh.epmiko(user)
                    print(f"Configuracion SNMP EXITOSA en {ip} {marca}.")

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
                            if id_list == "SN":
                                config_snmp.configurar_snmp_cisco(connection, community, permiso)
                                print(f"Configuracion SNMP EXITOSA en {ip} {marca}.")
                            else:
                                config_snmp.configurar_snmp_acl_cisco(connection, community, permiso, id_list)
                                print(f"Configuracion SNMP EXITOSA en {ip} {marca} con {id_list} como lista de acceso.")

                        elif marca == 'HPA5120':
                            if id_list == "SN":
                                config_snmp.configurar_snmp_hp(connection, community, permiso)
                                print(f"Configuracion SNMP EXITOSA en {ip} {marca}.")
                            else:
                                config_snmp.configurar_snmp_acl_hp(connection, community, permiso, id_list)
                                print(f"Configuracion SNMP EXITOSA en {ip} {marca} con {id_list} como lista de acceso.")
                        connection.disconnect()
            except Exception as e:
                print(f"Error al configurar el dispositivo {ip}: {e}")

base_path = "/home/paola/Documentos/loginapp/topologia/inventarios"
archivo = os.path.join(base_path, "datos_snmp.yaml")
datos_yaml = read_yaml.cargar_datos_snmp(archivo)
procesar_dispositivos_snmp(datos_yaml)
