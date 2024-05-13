#!/bin/bash

echo "EMPEZANDO CONFIGURACION"
cd /home/paola/Documentos/loginapp/topologia
nohup python3 mainv2.py > mi_log.log 2>&1 &

echo "CONFIGURACION EXITOSA"
