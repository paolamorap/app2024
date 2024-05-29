#!/bin/bash
echo ==============================================================
echo =================== GENERAR ARCHIVO JSON =====================
echo ==============================================================
# Definir la ruta al archivo
FILE_PATH="src/public/js/changes_flag.json"
# Crear el directorio si no existe
mkdir -p "$(dirname "$FILE_PATH")"
# Crear el archivo con el contenido especificado
echo '{"changes":false}' > "$FILE_PATH"
echo "Archivo $FILE_PATH creado con éxito."
echo ==============================================================
echo ==================== SCRIP COMPLETADO ========================
echo ==============================================================
