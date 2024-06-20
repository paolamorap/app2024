#!/bin/bash

# Verificar si se está ejecutando con privilegios de superusuario
if [ "$EUID" -ne 0 ]; then
  echo "Por favor, ejecute el script como superusuario (sudo)"
  exit 1
fi

# Instalar curl si no está instalado
echo ==============================================================
echo =================== INSTALACION DE CURL  =====================
echo ==============================================================
apt install -y curl

# Instalando Node.js y npm
echo ==============================================================
echo ==================== INSTALANDO NODE.JS ======================
echo ==============================================================
# Añadir el repositorio de NodeSource para Node.js v20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
# Instalar Node.js y npm
echo "--------------- *Intalando node.js y npm* ------------------"
apt install -y nodejs
# Verificar la versión de Node.js
NODE_VERSION=$(node -v)
NPM_VERSION=$(npm -v)
# Comprobar si la versión de Node.js es v20.x y npm es v10.x
if [[ "$NODE_VERSION" =~ ^v20\. && "$NPM_VERSION" =~ ^10\. ]]; then
  echo "Node.js y npm ya están en las versiones correctas."
else
  echo "Node.js version: $NODE_VERSION"
  echo "npm version: $NPM_VERSION"
fi

# Instalar las dependencias de node desde el package
echo "--------- *Intalando dependencias para node.js.* ------------"
npm install

echo ==============================================================
echo ===================== INSTALANDO PM2  ========================
echo ==============================================================
#Instalar PM2 globalmente:
npm install -g pm2

echo ==============================================================
echo ================== INICINADO APLICACION  =====================
echo ==============================================================
#Iniciar la aplicación con PM2:
pm2 start app.js
echo "-- *Verificar que el estado de la aplicacion sea exitoso.* --"
pm2 list

echo ==============================================================
echo ==================== SCRIP COMPLETADO ========================
echo ==============================================================