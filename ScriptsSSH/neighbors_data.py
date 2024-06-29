def neighbors_information (net_connect, interfacec):
    """
    Funcion que obtiene la informacion de los dispositivos que se encuentran conectados
    al dispositivo en el que se esta trabajando

    Datos de Ingreso:
    net_connect --> conexion ssh
    interfacec --> Diccionario con interfaces activas
    """

    try:
        output = net_connect.send_command('show spanning-tree detail')
        # Divide la salida en líneas
        lines = output.split('\n')
        # Diccionario para almacenar la información de cada interfaz
        interface_info = {}
        # Bandera para verificar si la línea actual contiene información relevante
        relevant_info = False
        # Variables para almacenar la información relevante
        designated_bridge = None
        designated_port_id = None
        # Para cada línea en la salida
        for line in lines:
            # Si la línea contiene alguna de las interfaces en la lista, activa la bandera
            for interface in interfacec:
                if interface in line:
                    relevant_info = True
                    current_interface = interface
                    interface_info[current_interface] = {}
            # Si la bandera está activada, extrae la información de 'Designated bridge' y 'Designated port id'
            if relevant_info:
                if 'Designated bridge' in line:
                    designated_bridge = line.split('address')[1].strip()
                elif 'Designated port id' in line:
                    designated_port_id = line.split('Designated port id is')[1].split(',')[0].strip()
                    # Almacena la información en el diccionario
                    interface_info[current_interface]= (designated_bridge, designated_port_id)
                    # Reinicia las variables para la próxima interfaz
                    designated_bridge = None
                    designated_port_id = None
                    relevant_info = False
        return interface_info
    except Exception as e:
        print(f"Error al obtener información STP: {e}")
        return {}