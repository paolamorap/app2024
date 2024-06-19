import bridge_id
import stp_info
import com_conex
import des_disp
import des_int_act
import map_int
import stp_blk
import verstp
import time 
import tree
import obt_infoyam
import dtsnmp
import bridge_id_root
import loadbalance
import json
import psutil
import os

def monitor_usage():
    pid = os.getpid()
    process = psutil.Process(pid)
    cpu_usage = process.cpu_percent(interval=1)
    memory_info = process.memory_info()
    memory_usage = memory_info.rss / (1024 ** 2)  # Convert to MB
    return cpu_usage, memory_usage

def datos_topologia(archivo_dispositivos):
    print("-------------- EJECUTANDO FASE 1 (RECOLECCION DE DATOS DEL YAML) ------------------")
    datos = obt_infoyam.infyam(archivo_dispositivos)
    direc = datos.keys() #Direcciones IP Filtradas

    print("------------------- EJECUTANDO FASE 2 (INFORMACION DE STP) ------------------------")
    time_datos_ini = time.time()
    b_id, f1, fif1 = bridge_id.bri_id(direc, datos)
    st_inf, f2, fif2 = stp_info.stp_inf(direc, datos)
    f = f1 or f2
    fif = dtsnmp.snmt(fif1, fif2)
    time_datos_fin = time.time()
    time_datos = time_datos_fin - time_datos_ini
    print('------------------------------------------------------------------------------------------------')
    print('El tiempo para almacenar datos es: ', time_datos)
    print('------------------------------------------------------------------------------------------------')

    print("--------------- EJECUTANDO FASE 3 (IDENTIFICACION DE CONEXIONES) -------------------")
    time_conexiones_ini = time.time()
    l = com_conex.b_conex(direc, b_id, st_inf) #Conexiones
    info_int, f3, fif3 = map_int.ma_int(direc, datos) #mapeo de interfaces 
    nf = verstp.obtener_numeros_despues_del_punto(l)
    nodb, f4, fif4 = stp_blk.stp_status(direc, nf, datos)
    ff = f1 or f2 or f3 or f4
    fif = dtsnmp.snmt(fif1, fif2, fif3, fif4)
    time_conexiones_fin = time.time()
    time_conexiones = time_conexiones_fin - time_conexiones_ini

    print('------------------------------------------------------------------------------------------------')
    print('El tiempo para obtener datos conexiones es: ', time_conexiones)
    print('------------------------------------------------------------------------------------------------')
    
    print("------------- EJECUTANDO FASE 4 (DATOS PARA EL DESPLIEGUE DEL ARBOL) -----------------")
    time_arbol_ini = time.time()
    bridge_id_root_dis = bridge_id_root.obtener_bridge_id_root_switch(direc, datos)
    root_bridge_id = bridge_id_root.obtener_bridge_id_root(bridge_id_root_dis)
    b_root = bridge_id_root.encontrar_ip_por_bridge_id(b_id, root_bridge_id) 
    bloq_int = tree.identificar_interfaces_bloqueadas(nodb, info_int)
    interconnections = tree.connection_tree_web(l, info_int)
    conexiones_blok = tree.marcar_puertos_bloqueados(interconnections, bloq_int)
    hostname = tree.obtener_hostname_dispositivos(direc, datos)
    info_disp = tree.informacion_dispositivos(archivo_dispositivos)
    discovered_hosts = tree.generate_switch_names(direc)
    time_arbol_fin = time.time()
    time_arbol = time_arbol_fin - time_arbol_ini
    print('------------------------------------------------------------------------------------------------')
    print('El tiempo para obtener datos para dibujar el arbol es: ', time_arbol)
    print('------------------------------------------------------------------------------------------------')
    
    return discovered_hosts, interconnections, b_root, conexiones_blok, hostname, info_disp

def good_luck_have_fun():
    nombreyaml = '/home/paola/Documentos/app2024/topologia/inventarios/dispositivos.yaml'
    discovered_hosts, interconnections, b_root, conexiones_blok, host_name, info_disp = datos_topologia(nombreyaml)
    time_archivos_ini = time.time()
    RUTA_ARCHIVO_TOPOLOGIA = r"/home/paola/Documentos/app2024/src/public/js/topology1.js"
    RUTA_ARCHIVO_DIFERENCIAS_TOPOLOGIA = r"/home/paola/Documentos/app2024/src/public/js/diff_topology.js"
    RUTA_ARCHIVO_TOPOLOGIA_CACHE = r"/home/paola/Documentos/app2024/src/public/js/cached_topology.json"
    CABECERA_ARCHIVO_TOPOLOGIA = f"\n\nvar topologyData = "
    DICCIONARIO_TOPOLOGIA = tree.generar_topologia_fija(discovered_hosts, interconnections, b_root, conexiones_blok, host_name, info_disp)
    TOPOLOGIA_CACHEADA = tree.leer_cache(RUTA_ARCHIVO_TOPOLOGIA_CACHE)
    tree.guardar_archivo_topologia(DICCIONARIO_TOPOLOGIA, CABECERA_ARCHIVO_TOPOLOGIA, RUTA_ARCHIVO_TOPOLOGIA)

    if TOPOLOGIA_CACHEADA:
        DATOS_DIFERENCIA = tree.generar_topologia_diferencias(TOPOLOGIA_CACHEADA, DICCIONARIO_TOPOLOGIA)
        tree.imprimir_diferencias(DATOS_DIFERENCIA)
        tree.guardar_archivo_topologia(DATOS_DIFERENCIA[2], CABECERA_ARCHIVO_TOPOLOGIA, dst=RUTA_ARCHIVO_DIFERENCIAS_TOPOLOGIA)

        # Verifica si hay cambios en los nodos o enlaces
        cambio_topologia = (len(DATOS_DIFERENCIA[0]['added']) > 0 or
                            len(DATOS_DIFERENCIA[0]['deleted']) > 0 or
                            len(DATOS_DIFERENCIA[1]['added']) > 0 or
                            len(DATOS_DIFERENCIA[1]['deleted']) > 0)
        if cambio_topologia:
            tree.guardar_cache(DICCIONARIO_TOPOLOGIA, RUTA_ARCHIVO_TOPOLOGIA_CACHE)
            with open('/home/paola/Documentos/app2024/src/public/js/changes_flag.json', 'w') as f:
                json.dump({'changes': True}, f)
    else:
        # Guarda la topología actual en el archivo de diferencias si falta el caché
        tree.guardar_archivo_topologia(DICCIONARIO_TOPOLOGIA, CABECERA_ARCHIVO_TOPOLOGIA, dst=RUTA_ARCHIVO_DIFERENCIAS_TOPOLOGIA)

    time_archivos_fin = time.time()
    time_archivos = time_archivos_fin - time_archivos_ini
    print('--------------------------------------------------------------------------------------------------')
    print('El tiempo para crear archivos de topologia es: ', time_archivos)
    print('--------------------------------------------------------------------------------------------------')

    print("-------------------- FINALIZO EL DESCUBRIMIENTO DE LA TOPOLOGIA --------------------")

if __name__ == '__main__':
    while True:
        time_main_ini = time.time()
        good_luck_have_fun()
        time_main_fin = time.time()
        time_main = time_main_fin - time_main_ini
        print('--------------------------------------------------------------------------------------------------')
        print('El tiempo para ejecutar el algoritmo de descubrimiento y graficacion de topologia es: ', time_main)
        print('--------------------------------------------------------------------------------------------------')

        # Monitor CPU and memory usage
        cpu_usage, memory_usage = monitor_usage()
        print('--------------------------------------------------------------------------------------------------')
        print(f'El uso del CPU es: {cpu_usage} %')
        print(f'El uso de la memoria es: {memory_usage} MB')
        print('--------------------------------------------------------------------------------------------------')

        time.sleep(30)  # Se corre cada un minuto
