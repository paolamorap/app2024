from ping3 import ping

def comprobar_dispositivo_activo(ip_address):
    """
    Realiza un ping al dispositivo para verificar su disponibilidad.
    """
    try:
        response = ping(ip_address, timeout=1)
        return response is not None
    except Exception as e:
        print(f"Error al realizar ping: {str(e)}")
        return False

def obtener_interfaces_up(net_connect):
    """
    Obtiene las interfaces del dispositivo que están en estado "up".
    """
    try:
        output = net_connect.send_command('show ip interface brief')
        interfaces_up = [line.split()[0] for line in output.splitlines() if len(line.split()) >= 6 and line.split()[5] == "up"]
        return interfaces_up
    except Exception as e:
        print(f"Error al obtener interfaces up: {e}")
        return []