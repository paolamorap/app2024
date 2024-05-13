import yaml

def infyam(nombre):
# Cargar el archivo YAML
    with open(nombre, "r") as archivo:
           datos = yaml.safe_load(archivo)
    # Inicializar un diccionario para almacenar las credenciales SSH y la comunidad SNMP
    # Inicializar un diccionario para almacenar las credenciales SSH y la comunidad SNMP
    credenciales_switches = {}

    # Obtener las credenciales SSH y la comunidad SNMP de todos los switches
    for categoria, configuracion in datos.items():
        if categoria.startswith('switchs_'):
            marca = categoria.replace('switchs_', '')  # Obtener la marca del switch
            for switch, detalles in configuracion['hosts'].items():
                if 'host' in detalles:
                    ip = detalles['host']
                    usuario = configuracion['vars'].get('user')
                    contraseña = configuracion['vars'].get('password')
                    snmp = configuracion['vars'].get('comunidad_snmp')
                    region_mstp = configuracion['vars'].get('region_mstp')
                    marca = configuracion['vars'].get('marca')
                    device_type = configuracion['vars'].get('device_type')
                    credenciales_switches[ip] = {'marca': marca, 'usuario': usuario, 'contraseña': contraseña, 'snmp': snmp, 
                                                 'region_mstp': region_mstp, 'device_type':device_type}

# Imprimir el diccionario de credenciales SSH y SNMP para todos los switches
    return credenciales_switches