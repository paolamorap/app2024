#!/bin/bash

# Verificar si el script se está ejecutando con privilegios de superusuario
if [ "$EUID" -ne 0 ]; then
  echo "Por favor, ejecute el script como superusuario (sudo ./install_packages.sh)"
  exit 1
fi

echo ==============================================================
echo ============ INSTALANDO DEPENDENCIAS DE PYTHON ===============
echo ==============================================================
# Asegurarse de que Python 3 y pip estén instalados
echo "Verificando la instalación de Python 3 y pip..."
apt update
apt install -y python3 python3-pip

# Lista de paquetes a instalar con versiones específicas
packages=(
  "influxdb==5.3.2"
  "netmiko==4.3.0"
  "networkx==3.3"
  "numpy==1.26.4"
  "paramiko==3.4.0"
  "ping3==4.0.8"
  "pysnmp==4.4.12"
  "pyTelegramBotAPI==4.18.1"
  "PyYAML==6.0.1"
)

# Instalar cada paquete usando pip
echo "Instalando paquetes de Python..."
for package in "${packages[@]}"; do
  pip3 install "$package"
done

echo ==============================================================
echo =================== INSTALACION EXITOSA ======================
echo ==============================================================
