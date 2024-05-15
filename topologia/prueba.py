import yaml

def generar_yaml(conexiones):
    # Diccionario que contendrá todas las conexiones
    conexiones_dict = {'conexiones_disp': {}}

    # Iterar sobre cada grupo de conexiones
    for idx, grupo in enumerate(conexiones, start=1):
        conexion_key = f'conexion{idx}'
        conexiones_dict['conexiones_disp'][conexion_key] = {}
        host_index = 1

        # Iterar sobre cada conexión individual en el grupo
        for host_info in grupo:
            ip, interfaz, ip_destino, interfaz_destino = host_info
            host_key = f'host{host_index}'
            host_index += 1
            conexiones_dict['conexiones_disp'][conexion_key][host_key] = {
                'IP': ip,
                'interfaz1': interfaz
            }
            host_key = f'host{host_index}'
            host_index += 1
            conexiones_dict['conexiones_disp'][conexion_key][host_key] = {
                'IP': ip_destino,
                'interfaz1': interfaz_destino
            }

    # Escribir el diccionario a un archivo YAML
    with open('conexiones.yaml', 'w') as file:
        yaml.dump(conexiones_dict, file, sort_keys=False, default_flow_style=False)

# Lista de ejemplo con conexiones
conexiones = [
    [('192.168.20.4', 'G0/2', '192.168.20.3', 'G0/1')],
    [('192.168.20.4', 'G1/1', '192.168.20.3', 'G0/2')],
    [('192.168.20.4', 'G0/3', '192.168.20.5', 'G0/2'), ('192.168.20.2', 'G0/2', '192.168.20.4', 'G1/0'), ('192.168.20.10', 'G0/2', '192.168.20.5', 'G1/0')]
]

generar_yaml(conexiones)
