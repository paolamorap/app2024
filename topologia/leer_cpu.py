import yaml

def crear_diccionario_host_marca(archivo):
    """
    Función para leer archivos yaml - Complemento de cpu.py

    Parameters:
    archivo(str):       Ruta de archivo yaml con información de los dispositivos

    Return:
    diccionario(dict)   Diccionario con los datos del archivo yaml
    """
    diccionario = {}
    with open(archivo, 'r') as file:
        data = yaml.safe_load(file)
        for grupo, info_grupo in data.items():
            for host, info_host in info_grupo['hosts'].items():
                diccionario[info_host['host']] = grupo

    return diccionario