from netmiko import ConnectHandler
import neighbors_data
import active_device
import current_device_data

def establecer_conexion(ip_address, username, password):
    """
    Funcion que se encarga de establece una conexión SSH con el dispositivo
    empleando la libreria Netmiko.

    ip_address --> direccion IP del dispositivo
    username --> nombre del dispositivo
    passwprd --> contrasena para ingresar al dispositivo
    """
    device_info = {
        'device_type': 'cisco_ios',
        'ip': ip_address,
        'username': username,
        'password': password,
    }
    try:
        return ConnectHandler(**device_info)
    except Exception as e:
        print(f"Error en {ip_address}: {e}")
        return None

def process_device(ip_address, username, password):

    try:
        net_connect = establecer_conexion(ip_address, username, password)
        if not net_connect:
            raise ConnectionError("Failed to establish SSH connection.")

        if not active_device.comprobar_dispositivo_activo(ip_address):
            net_connect.disconnect()
            raise ValueError("Device is not active.")

        interfaces_up = active_device.obtener_interfaces_up(net_connect)
        block_ports_device = current_device_data.blocked_interface_device(net_connect)
        info_vecinos = neighbors_data.neighbors_information(net_connect, interfaces_up)
        mac_bridge_id, info_disp = current_device_data.device_information(net_connect, interfaces_up)

        net_connect.disconnect()

        return info_vecinos, mac_bridge_id, info_disp, block_ports_device

    except Exception as e:
        print(f"Error al procesar dispositivo {ip_address}: {e}")
        return None, None, None, None