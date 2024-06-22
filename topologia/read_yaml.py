import yaml
from yaml.loader import SafeLoader


# Función para leer el archivo YAML
def leer_yaml(ruta):
    """
    Esta función devuelve los datos del archivo yaml en formato de diccionario.

    Parámetros:
    ruta (str): Ruta del archivo .yaml

    Retorna:
    datos: Datos en formato diccionario.
    """
    with open(ruta, 'r') as archivo:
        datos = yaml.safe_load(archivo)
    return datos

def cargar_datos_snmp(filepath):
    try:
        with open(filepath, 'r') as file:
            return yaml.load(file, Loader=SafeLoader)
    except Exception as e:
        print(f"Error al cargar el archivo YAML: {e}")
        return None