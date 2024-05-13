import conexion_ssh
import config_acl
import os
import read_yaml

def procesar_dispositivos_accesslist(datos_yaml):
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
                    config_acl.configurar_acl_3com(ip, user, password, n_rule, id_list, ip_red, mascara_wildcard)
                    print(f"Access List {id_list} creado EXITOSAMENTE en {ip} {marca}.")

                elif marca == 'TPLINK':
                    config_acl.comandos_acl_tplink(n_rule, id_list, ip_red, mascara_wildcard)
                    conexion_ssh.epmiko(user)
                    print(f"Access List {id_list} creado EXITOSAMENTE en {ip} {marca}.")

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
                            config_acl.configurar_acl_cisco(connection, id_list, ip_red, mascara_wildcard)
                            print(f"Access List {id_list} creado EXITOSAMENTE en {ip} {marca}.")

                        elif marca == 'HPA5120':
                            config_acl.configurar_acl_hp(connection, n_rule, id_list, ip_red, mascara_wildcard)
                            print(f"Access List {id_list} creado EXITOSAMENTE en {ip} {marca}.")
                        connection.disconnect()
            except Exception as e:
                print(f"Error al configurar el dispositivo {ip}: {e}")

base_path = "/home/paola/Documentos/loginapp/topologia/inventarios"
archivo = os.path.join(base_path, "datos_access_list.yaml")
datos_yaml = read_yaml.cargar_datos_snmp(archivo)
procesar_dispositivos_accesslist(datos_yaml)
