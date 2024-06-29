import re

def convertir_nombres_interfaces(interfaces_up):
    interfaces_abreviadas = []
    for interface in interfaces_up:
        indice_digito = next((index for index, char in enumerate(interface) if char.isdigit()), None)
        if indice_digito is not None:
            prefijo = interface[:indice_digito]
            sufijo = interface[indice_digito:]
            prefijo_abreviado = prefijo.replace("GigabitEthernet", "Gi")
            interface_abreviada = prefijo_abreviado + sufijo
            interfaces_abreviadas.append(interface_abreviada)
        else:
            interfaces_abreviadas.append(interface)
    return interfaces_abreviadas

def device_information(net_connect, interfaces):

    interfaces_up = convertir_nombres_interfaces(interfaces)

    try:
        output_stp = net_connect.send_command('show spanning-tree')
        bridge_id_pattern = r'Bridge ID\s+Priority\s+\d+\s+\(priority\s+\d+\s+sys-id-ext\s+\d+\)\s+Address\s+(\S+)'
        match_bridge_id = re.search(bridge_id_pattern, output_stp)
        mac_bridge_id = match_bridge_id.group(1) if match_bridge_id else None

        device_data = {}
        if mac_bridge_id:
            for interface in interfaces_up:
                interface_pattern = rf'{re.escape(interface)}\s+\w+\s+(\w+)\s+\d+\s+(\d+\.\d+)\s+Shr'
                match = re.search(interface_pattern, output_stp)
                prio_nbr = match.group(2) if match else None
                device_data [interface] = (mac_bridge_id, prio_nbr)

        return mac_bridge_id, device_data

    except Exception as e:
        print(f"Error al obtener información STP: {e}")
        return None, None

def blocked_interface_device(net_connect):

    try:
        blocked_ports = net_connect.send_command('show spanning-tree blockedports | include /')
        interface_blocked = [line.split()[1] for line in blocked_ports.splitlines() if '/' in line.lower()]
        return interface_blocked
    except Exception as e:
        print(f"Error al obtener interfaces bloqueadas: {e}")
        return []