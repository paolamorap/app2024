import bridge_id
import stp_info
import com_conex
import map_int
import stp_blk
import verstp
import time 
import tree
import obt_infoyam
import dtsnmp
import bridge_id_root
import loadbalance



def ejecutar_proceso(direc, datos):
    print("----------Inicio Descubriendo Topologia---------------")
    print("-------------FASE 1 -----------------")
    
    print("Ejecutando Fase 2 - Almacenamiento de Datos")
    b_id, f1, fif1 = bridge_id.bri_id(direc, datos)
    st_inf, f2, fif2 = stp_info.stp_inf(direc, datos)
    f = f1 or f2
    fif = dtsnmp.snmt(fif1, fif2)

    print("Ejecutando Fase 3 - Identificacion de Conexiones")
    l = com_conex.b_conex(direc, b_id, st_inf)
    info_int, f3, fif3 = map_int.ma_int(direc, datos)
    nf = verstp.obtener_numeros_despues_del_punto(l)
    nodb, f4, fif4 = stp_blk.stp_status(direc, nf, datos)
    ff = f1 or f2 or f3 or f4
    fif = dtsnmp.snmt(fif1, fif2, fif3, fif4)

    print("Ejecutando Fase 4 - Despliegue del Arbol")
    bridge_id_root_dis = bridge_id_root.obtener_bridge_id_root_switch(direc, datos)
    root_bridge_id = bridge_id_root.obtener_bridge_id_root(bridge_id_root_dis)
    b_root = bridge_id_root.encontrar_ip_por_bridge_id(b_id, root_bridge_id)
    bloq_int = tree.identificar_interfaces_bloqueadas(nodb, info_int)
    interconnections = tree.connection_tree_web(l, info_int)
    conexiones_blok = tree.marcar_puertos_bloqueados(interconnections, bloq_int)
    info_disp = tree.obtener_informacion_dispositivos(direc, datos)
    discovered_hosts = tree.generate_switch_names(direc)

    TOPOLOGY_FILE_PATH = r"/home/paola/Documentos/app2024/src/public/js/topology.js"
    TOPOLOGY_FILE_HEAD = f"\n\nvar topologyData = "
    TOPOLOGY_DICT = tree.generate_topology_json(discovered_hosts, interconnections,b_root,conexiones_blok, info_disp) 
    tree.write_topology_file(TOPOLOGY_DICT,TOPOLOGY_FILE_HEAD,TOPOLOGY_FILE_PATH) 
    print("------------FIN----------")
    # Preparar los datos para devolver
    return l, nodb, info_int, ff, fif


nombreyaml = '/home/paola/Documentos/app2024/topologia/inventarios/dispositivos.yaml'
datos = obt_infoyam.infyam(nombreyaml)
direc = datos.keys()  # Direcciones IP Filtradas

l, nodb, info_int, ff, fif = ejecutar_proceso(direc, datos)
