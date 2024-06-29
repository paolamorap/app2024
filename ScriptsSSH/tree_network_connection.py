import ssh_connection
from multiprocessing import Process, Manager

def process_device(ip_address, username, password, results):
    result = ssh_connection.process_device(ip_address, username, password)
    results[ip_address] = result

def general_data_device(username, password, ip_list):
    device_data = {}
    neighbor_device_data = {}
    blocked_ports_current_device = {}

    for server_ip in ip_list:
        try:
            info_vecinos, mac_bridge_id, info_disp, block_ports_device = ssh_connection.process_device(server_ip, username, password)            
            device_data[(server_ip, mac_bridge_id)] = info_disp
            neighbor_device_data[(server_ip, mac_bridge_id)] = info_vecinos
            blocked_ports_current_device[server_ip] = block_ports_device
        except ValueError as e:
            print(f"Error al procesar dispositivo {server_ip}: {e}")
        except Exception as e:
            print(f"Error general al procesar dispositivo {server_ip}: {e}")

    return device_data, neighbor_device_data, blocked_ports_current_device


def general_data_device1(username, password):
    device_data = {}
    neighbor_device_data = {}
    blocked_ports_current_device = {}

    for n in range(1, 6):
        server_ip = f"10.0.1.{n}"
        info_vecinos, mac_bridge_id, info_disp, block_ports_device = ssh_connection.process_device(server_ip, username, password)
        device_data[(server_ip, mac_bridge_id)] = info_disp
        neighbor_device_data[(server_ip, mac_bridge_id)] = info_vecinos
        blocked_ports_current_device[server_ip] = block_ports_device    

    return device_data, neighbor_device_data, blocked_ports_current_device



def identify_connection_exit(salida_final):
    salida_modificada = {}
    for key, value in salida_final.items():
        modified_value = [v.replace('GigabitEthernet', 'Gi') for v in value]
        salida_modificada[key] = modified_value
    return salida_modificada

def identify_connections(device_data, neighbors_data):
    device_connections = {}
    int_device_connections = {}
    int_device_connections_mod ={}

    for (dispositivo, mac_dispositivo_actual), current_data in device_data.items():
        device_connections[dispositivo] = []  # Inicializa una lista vacía para almacenar las conexiones entre dispositivos
        for (vecino_dispositivo, mac_disp_vecino), vecino_data in neighbors_data.items():
            if dispositivo != vecino_dispositivo:  # Evitar comparar el dispositivo consigo mismo
                if vecino_data:  # Verificar si vecino_data contiene elementos
                    for int_vecino, (mac_vecino, port_vecino) in vecino_data.items():
                        if mac_vecino == mac_dispositivo_actual:
                            device_connections[dispositivo].append(vecino_dispositivo)  # Agrega la conexión a la lista
                            for int_dispositivo_actual, (mac_int_dispositivo_actual, port_int_dispositivo_actual) in current_data.items():
                                if port_vecino == port_int_dispositivo_actual: #Compara la conexion entre puertos
                                    int_device_connections[(dispositivo, int_dispositivo_actual)] = [vecino_dispositivo, int_vecino]  #Agrega las conexiones por interfaces y dispositivos

        int_device_connections_mod = identify_connection_exit(int_device_connections)

    return device_connections, int_device_connections_mod




