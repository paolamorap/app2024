def fil_bid(nombre):
    """
    Función para filtrar la informacion de b_id.txt
    Se obtiene el bridge ID de dispositivos TPLink

    Parameters:
    nombre(str):    Ruta del archivo b_id.txt

    Return:
    bid(dict):      Diccionario con los bridge ID
    """
    file_name = nombre
    # Variables para almacenar la dirección del puente designado
    direccion_designated_bridge = None

    # Abrir el archivo y leer todas las líneas
    with open(file_name, 'r') as file:
        lines = file.readlines()
    f = 0
    bid = {}
    # Iterar sobre las líneas para encontrar la dirección del puente designado
    for line in lines:
        # Buscar la línea que contiene "Designated Bridge"
        if "Designated Bridge" in line:
            # Extraer la dirección del puente designado
            f = 1
        # Si ya se ha encontrado la línea que contiene "Designated Bridge", buscar la línea que contiene "Address"
        elif "Conectando al host" in line:
            # Verificar si la línea se puede dividir correctamente
            parts = line.split(":")
            if len(parts) > 1:
                dk = parts[1].strip()

        elif "Address" in line and f == 1:
            # Verificar si la línea se puede dividir correctamente
            parts = line.split(":")
            if len(parts) > 1:
                dv = parts[1].strip().replace("-","")
                f = 0
                bid[dk] = dv

    return bid