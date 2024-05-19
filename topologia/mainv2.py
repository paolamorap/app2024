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

# Ingreso de Parametros - Comunidad SNMP, Direcciones IP
#Fase 1
print("-------------FASE 1 -----------------")
nombreyaml = '/home/paola/Documentos/app2024/topologia/inventarios/dispositivos.yaml'
datos = obt_infoyam.infyam(nombreyaml)
direc = datos.keys() #Direcciones IP Filtradas
print(direc)

print("Ejecutando Fase 2 - Almacenamiento de Datos")
#Fase 2
#Informacion STP
# Bridge ID, Designed Bridge
b_id,f1,fif1 = bridge_id.bri_id(direc,datos)
st_inf,f2,fif2 = stp_info.stp_inf(direc,datos)
f = f1 or f2

fif = dtsnmp.snmt(fif1,fif2)

#print (b_id)
#print(st_inf)
print("Ejecutando Fase 3 - Identificacion de Conexiones")
#Fase 3
#Identificación de Conexiones
l = com_conex.b_conex(direc,b_id,st_inf)
#print('CONEXIONES',l)

#Mapeo de Las etiquetas
info_int,f3,fif3 = map_int.ma_int(direc,datos)

print('INTERFACES',info_int)

nf = verstp.obtener_numeros_despues_del_punto(l)

nodb,f4,fif4=stp_blk.stp_status(direc,nf,datos)

ff = f1 or f2 or f3 or f4
fif = dtsnmp.snmt(fif1,fif2,fif3,fif4)


#Fase 4 - Despligue del arbol en la web
print("Ejecutando Fase 4 - Despliegue del Arbol")

bridge_id_root_dis =  bridge_id_root.obtener_bridge_id_root_switch(direc, datos)
root_bridge_id = bridge_id_root.obtener_bridge_id_root(bridge_id_root_dis)
b_root = bridge_id_root.encontrar_ip_por_bridge_id(b_id,root_bridge_id) 
print('B ROOT', b_root)
bloq_int=tree.identificar_interfaces_bloqueadas(nodb, info_int)
interconnections = tree.connection_tree_web(l,info_int)
#print('INTERCONEXIONES', interconnections)

conexiones_blok = tree.marcar_puertos_bloqueados(interconnections, bloq_int)
#print('CONEXION BLOCKS', conexiones_blok)
#info_disp1 = tree.obtener_informacion_dispositivos(direc,datos)
info_disp = tree.informacion_dispositivos(nombreyaml)
print('INFO DISP', info_disp)
discovered_hosts = tree.generate_switch_names(direc)
print('HOSTSS', discovered_hosts)


OUTPUT_TOPOLOGY_FILENAME = 'topology.js'
TOPOLOGY_FILE_PATH = r"/home/paola/Documentos/app2024/src/public/js/topology.js"
TOPOLOGY_FILE_HEAD = f"\n\nvar topologyData = "
TOPOLOGY_DICT = tree.generate_topology_json1(discovered_hosts, interconnections,b_root,conexiones_blok, info_disp) 
tree.write_topology_file(TOPOLOGY_DICT,TOPOLOGY_FILE_HEAD,TOPOLOGY_FILE_PATH) 

s, dp = loadbalance.ob_yaml(l,nodb,info_int)

loadbalance.yaml_web(dp)
loadbalance.yaml_datos(s)

print("------------FIN----------")


