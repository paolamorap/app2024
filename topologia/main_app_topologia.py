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

def datos_topologia(archivo_dispositivos):
    print("-------------- EJECUTANDO FASE 1 (RECOLECCION DE DATOS DEL YAML) -----------------)")
    datos = obt_infoyam.infyam(archivo_dispositivos)
    direc = datos.keys() #Direcciones IP Filtradas
    #print(direc)

    print("------------------- EJECUTANDO FASE 2 (INFORMACION DE STP) ------------------------)")
    b_id,f1,fif1 = bridge_id.bri_id(direc,datos)
    #print(b_id)
    st_inf,f2,fif2 = stp_info.stp_inf(direc,datos)
    f = f1 or f2
    fif = dtsnmp.snmt(fif1,fif2)
    #print(st_inf)

    print("--------------- EJECUTANDO FASE 3 (IDENTIFICACION DE CONEXIONES) ------------------)")
    l = com_conex.b_conex(direc,b_id,st_inf)
    #print('CONEXIONES',l)
    #Mapeo de Las etiquetas
    info_int,f3,fif3 = map_int.ma_int(direc,datos)
    #print('INTERFACES',info_int)
    nf = verstp.obtener_numeros_despues_del_punto(l)
    nodb,f4,fif4=stp_blk.stp_status(direc,nf,datos)
    ff = f1 or f2 or f3 or f4
    fif = dtsnmp.snmt(fif1,fif2,fif3,fif4)

    print("------------- EJECUTANDO FASE 4 (DATOS PARA EL DESPLIEGUE DEL ARBOL) ----------------)")
    bridge_id_root_dis =  bridge_id_root.obtener_bridge_id_root_switch(direc, datos)
    root_bridge_id = bridge_id_root.obtener_bridge_id_root(bridge_id_root_dis)
    b_root = bridge_id_root.encontrar_ip_por_bridge_id(b_id,root_bridge_id) 
    bloq_int=tree.identificar_interfaces_bloqueadas(nodb, info_int)
    interconnections = tree.connection_tree_web(l,info_int)
    
    conexiones_blok = tree.marcar_puertos_bloqueados(interconnections, bloq_int)
    hostname = tree.obtener_hostname_dispositivos(direc,datos)
    info_disp = tree.informacion_dispositivos(archivo_dispositivos)
    discovered_hosts = tree.generate_switch_names(direc)
    print('--------------------------DATOS ARBOL---------------------------------')
    print('----------------------------------------------------------------------------------')
    print('DISCOVERT HOSTSS', discovered_hosts)
    print('----------------------------------------------------------------------------------')
    print("INTERCONNECTIONS:", interconnections)
    print('----------------------------------------------------------------------------------')
    print('BR_OOT', b_root)
    print('----------------------------------------------------------------------------------')
    print('CONEXION BLOCKS', conexiones_blok)
    print('----------------------------------------------------------------------------------')
    print('HOST NAME', hostname)
    print('----------------------------------------------------------------------------------')
    print('INFO DISP', info_disp)
    print('----------------------------------------------------------------------------------')
    
    return discovered_hosts, interconnections, b_root, conexiones_blok, hostname, info_disp



def good_luck_have_fun():
    
    nombreyaml = '/home/paola/Documentos/app2024/topologia/inventarios/dispositivos.yaml'
    discovered_hosts, interconnections, b_root, conexiones_blok, host_name, info_disp = datos_topologia(nombreyaml)
    """
    TOPOLOGY_FILE_PATH = r"/home/paola/Documentos/app2024/src/public/js/topology1.js" 
    TOPOLOGY_DIFF_PATH = r"/home/paola/Documentos/app2024/src/public/js/diff_topology.js"
    CACHED_TOPOLOGY_FILENAME = r"/home/paola/Documentos/app2024/src/public/js/cached_topology.json" 

    TOPOLOGY_FILE_HEAD = f"\n\nvar topologyData = "
    TOPOLOGY_DICT = tree.generar_topologia_fija(discovered_hosts, interconnections,b_root,conexiones_blok, host_name, info_disp) #TOPOLOGY 1
    CACHED_TOPOLOGY = tree.leer_cache(CACHED_TOPOLOGY_FILENAME) 
    tree.guardar_archivo_topologia(TOPOLOGY_DICT,TOPOLOGY_FILE_HEAD,TOPOLOGY_FILE_PATH)   

    if CACHED_TOPOLOGY:
        DIFF_DATA = tree.generar_topologia_diferencias(CACHED_TOPOLOGY, TOPOLOGY_DICT)
        tree.print_diff(DIFF_DATA)
        tree.guardar_archivo_topologia(DIFF_DATA[2], TOPOLOGY_FILE_HEAD, dst=TOPOLOGY_DIFF_PATH)

        # Verifica si hay cambios en los nodos o enlaces
        topologia_cambio = (len(DIFF_DATA[0]['added']) > 0 or
                            len(DIFF_DATA[0]['deleted']) > 0 or
                            len(DIFF_DATA[1]['added']) > 0 or
                            len(DIFF_DATA[1]['deleted']) > 0)
        if topologia_cambio:
            tree.guardar_cache(TOPOLOGY_DICT, CACHED_TOPOLOGY_FILENAME)
            with open('/home/paola/Documentos/app2024/src/public/js/changes_flag.json', 'w') as f:
                json.dump({'changes': True}, f)

    else:
        #escribe la topología actual en el archivo de diferencias si falta el caché
        tree.guardar_archivo_topologia(TOPOLOGY_DICT, dst=TOPOLOGY_DIFF_PATH)
    """

    RUTA_ARCHIVO_TOPOLOGIA = r"/home/paola/Documentos/app2024/src/public/js/topology1.js"
    RUTA_ARCHIVO_DIFERENCIAS_TOPOLOGIA = r"/home/paola/Documentos/app2024/src/public/js/diff_topology.js"
    RUTA_ARCHIVO_TOPOLOGIA_CACHE = r"/home/paola/Documentos/app2024/src/public/js/cached_topology.json"

    CABECERA_ARCHIVO_TOPOLOGIA = f"\n\nvar topologyData = "
    DICCIONARIO_TOPOLOGIA = tree.generar_topologia_fija(discovered_hosts, interconnections,b_root,conexiones_blok, host_name, info_disp)
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

    print("-------------------- FINALIZO EL DESCUBRIMIENTO DE LA TOPOLOGIA --------------------")

if __name__ == '__main__':
    while True:
        good_luck_have_fun()
        time.sleep(100)  # Se corre cada un minuto

