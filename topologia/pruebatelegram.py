import os

# Define el directorio del archivo actual
current_dir = os.path.dirname(__file__)

# Sube un nivel en el directorio
parent_dir = os.path.dirname(current_dir)

# Define el segmento adicional
segmento_adicional = "balanceo/balanceo_web.yaml"

# Combina el directorio padre con el segmento adicional
ruta_completa = os.path.join(current_dir, segmento_adicional)

print(ruta_completa)
