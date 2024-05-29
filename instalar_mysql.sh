#!/bin/bash

# Verificar si se está ejecutando con privilegios de superusuario
if [ "$EUID" -ne 0 ]; then
  echo "Por favor, ejecute el script como superusuario (sudo ./instalar_mysql.sh)"
  exit 1
fi

echo ==============================================================
echo ==================== INSTALANDO MYSQL  =======================
echo ==============================================================
apt update
apt install -y mysql-server

echo ==============================================================
echo =========== MYSQL INSTALADO CORRECTAMENTE  ===================
echo ==============================================================

systemctl start mysql.service
systemctl enable mysql.service

if systemctl is-active --quiet mysql.service; then
  echo "Servicio MySQL está activo."
else
  echo "Error: el servicio MySQL no se inició correctamente."
  exit 1
fi

echo ==============================================================
echo =============== CONFIGURANDO USUARIO ROOT ====================
echo ==============================================================

echo "Configurando usuario root de MySQL..."
mysql <<EOF
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'admin';
EOF
echo "Usuario root configurado."

echo "Creando archivo de configuración temporal de MySQL..."
cat <<EOF >~/.my.cnf
[client]
user=root
password=admin
EOF
chmod 600 ~/.my.cnf

echo ==============================================================
echo ============= CREANDO BASE DE DATOS Y TABLA ==================
echo ==============================================================

echo "Creando base de datos y tabla..."
mysql <<EOF
CREATE DATABASE epolaris;
USE epolaris;
CREATE TABLE users (
  email VARCHAR(255) NOT NULL,
  name VARCHAR(50) NOT NULL,
  password VARCHAR(255) NOT NULL,
  is_default_password TINYINT(1) NOT NULL DEFAULT 1,
  privilege VARCHAR(20) NOT NULL DEFAULT 'user',
  username VARCHAR(255),
  PRIMARY KEY (email),
  UNIQUE (username)
);
INSERT INTO users (email, name, password, privilege, is_default_password, username)
VALUES ('admin@example.com', 'Admin User', '\$2b\$10\$dA.jNSzAuUD74oC.4aGIeuPfQUZbBxCp7Ksmx/kAXjC3XDkZTdQrC', 'admin', TRUE, 'admin');
EOF
echo "Base de datos y tabla creadas."

echo "Eliminando archivo de configuración temporal de MySQL..."
rm -f ~/.my.cnf

echo ==============================================================
echo ==================== SCRIP COMPLETADO ========================
echo ==============================================================
