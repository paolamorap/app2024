import bridge_id
import stp_info
import com_conex
import map_int
import stp_blk
import verstp
import time
import obt_infoyam
import obt_root
import bridge_id_root
import tree
import dtsnmp
import json
import obt_tplink

def main_top(direc):
    print("-------------------- EMPIEZA EL DESCUBRIMIENTO DE LA TOPOLOGIA ---------------------")
    print("-------------- EJECUTANDO FASE 1 (RECOLECCION DE DATOS DEL YAML) -------------------")
    #print("Ejecutando Fase 1 - Lectura de Archivo de Configuraciones")
    #Fase 1
    #Lectura de Archivo Yaml - Configuraciones
    archivoDispositivos = "/home/paola/Documentos/app2024/topologia/inventarios/dispositivos.yaml"
    datos = obt_infoyam.infyam(archivoDispositivos)
    iptp,credenciales = obt_tplink.filtplink(archivoDispositivos)
    b_root = obt_root.obtr(datos,iptp)
    print(datos)
    print(direc)
    print("------------------- EJECUTANDO FASE 2 (INFORMACION DE STP) --------------------------")
    #Fase 2
    #Informacion STP
    # Bridge ID, Designed Bridge
    
    b_id,f1,fif1= bridge_id.bri_id(direc,datos)
    st_inf,f2,fif2 = stp_info.stp_inf(direc,datos)

    """
    #Proceso extra para conmutadores TPLINK

    f.epmiko(credenciales[iptp[0]]["usuario"],credenciales[iptp[0]]["contraseña"], iptp)
    tp_d = leer.fil_bid("b_id.txt")
    stn = tp_linkssh.tplink_id(b_root,st_inf,tp_d,iptp)
    """

    print("--------------- EJECUTANDO FASE 3 (IDENTIFICACION DE CONEXIONES) --------------------")
    #Fase 3 - Identificación de Conexiones
    l = com_conex.b_conex(direc,b_id,st_inf)
    #print(l)
    #Mapeo de Las etiquetas
    info_int,f3,fif3 = map_int.ma_int(direc,datos)
    #print(info_int)
    nf = verstp.obtener_numeros_despues_del_punto(l)
    #print(nf)
    nodb,f4,fif4=stp_blk.stp_status(direc,nf,datos)
    #print(nodb)
    ff = f1 or f2 or f3 or f4
    fif = dtsnmp.snmt(fif1,fif2,fif3,fif4)
    
    print("------------- EJECUTANDO FASE 4 (DATOS PARA EL DESPLIEGUE DEL ARBOL) -----------------")
    #Fase 4 - Despligue del arbol en la web
    bridge_id_root_dis =  bridge_id_root.obtener_bridge_id_root_switch(direc, datos)
    root_bridge_id = bridge_id_root.obtener_bridge_id_root(bridge_id_root_dis)
    b_root_punta = bridge_id_root.encontrar_ip_por_bridge_id(b_id,root_bridge_id)
    bloq_int=tree.identificar_interfaces_bloqueadas(nodb, info_int)
    interconnections = tree.connection_tree_web(l,info_int)
    conexiones_blok = tree.marcar_puertos_bloqueados(interconnections, bloq_int)
    hostname = tree.obtener_hostname_dispositivos(direc,datos)
    info_disp = tree.informacion_dispositivos(archivoDispositivos)
    discovered_hosts = tree.generate_switch_names(direc)

    print("------------- EJECUTANDO FASE 5 (GENERANDO ARCHIVOS DE DESPLIEGUE) -------------------")

    RUTA_ARCHIVO_TOPOLOGIA = r"/home/paola/Documentos/app2024/src/public/js/topology1.js"
    RUTA_ARCHIVO_DIFERENCIAS_TOPOLOGIA = r"/home/paola/Documentos/app2024/src/public/js/diff_topology.js"
    RUTA_ARCHIVO_TOPOLOGIA_CACHE = r"/home/paola/Documentos/app2024/src/public/js/cached_topology.json"

    CABECERA_ARCHIVO_TOPOLOGIA = f"\n\nvar topologyData = "
    DICCIONARIO_TOPOLOGIA = tree.generar_topologia_fija(discovered_hosts, interconnections,b_root_punta,conexiones_blok, hostname, info_disp)
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
        tree.guardar_archivo_topologia(DICCIONARIO_TOPOLOGIA, dst=RUTA_ARCHIVO_DIFERENCIAS_TOPOLOGIA)

    print("-------------------- FINALIZO EL DESCUBRIMIENTO DE LA TOPOLOGIA ----------------------")
    
    return l,ff,fif