
import yaml
from yaml.loader import SafeLoader

def cargar_configuracion_yaml(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        return yaml.safe_load(archivo)


def cargar_datos_snmp(filepath):
    try:
        with open(filepath, 'r') as file:
            return yaml.load(file, Loader=SafeLoader)
    except Exception as e:
        print(f"Error al cargar el archivo YAML: {e}")
        return None