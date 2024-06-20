#!/bin/bash

echo "=============================================================="
echo "================= INICIANDO DOCKER COMPOSE ==================="
echo "=============================================================="

# Verificar si se está ejecutando con privilegios de superusuario
if [ "$EUID" -ne 0 ]; then
  echo "Por favor, ejecute el script como superusuario (sudo)"
  exit 1
fi

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null
then
  echo "Docker no está instalado. Instalando Docker..."
  apt-get update
  apt-get install -y docker.io
  systemctl start docker
  systemctl enable docker
else
  echo "Docker ya está instalado."
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null
then
  echo "Docker Compose no está instalado. Instalando Docker Compose..."
  curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  chmod +x /usr/local/bin/docker-compose
  ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
else
  echo "Docker Compose ya está instalado."
fi

cd ..
cd Docker_Monitoreo
docker-compose up -d

echo "=============================================================="
echo "==================== SCRIPT COMPLETADO ======================="
echo "=============================================================="
