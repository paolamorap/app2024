import configuracion_inicial

ruta_datos = r'/home/du/Auto_Mon_2024_Cod/Automatizacion_Red_2024/epops/inventarios/conf_inicial.yaml'
datos = configuracion_inicial.cargar_configuracion_yaml(ruta_datos)
configuracion_inicial.procesar_dispositivos(datos)