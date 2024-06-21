#!/bin/bash

echo "EMPEZANDO CONFIGURACION"

# Buscar el directorio app2024/topologia
DIRECTORIO_BASE=$(find / -type d -name "topologia" -path "*/app2024/topologia" 2>/dev/null | head -n 1)

if [ -z "$DIRECTORIO_BASE" ]; then
  echo "No se pudo encontrar el directorio app2024/topologia"
  exit 1
fi

# Mostrar el directorio encontrado
echo "Directorio encontrado: $DIRECTORIO_BASE"

# Cambiar al directorio encontrado
cd "$DIRECTORIO_BASE" || { echo "Error al cambiar al directorio $DIRECTORIO_BASE"; exit 1; }

# Ejecutar el script Python con nohup
nohup python3 mon3.py > mi_log.log 2>&1 &

echo "CONFIGURACION EXITOSA"
