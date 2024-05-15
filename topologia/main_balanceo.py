import loadbalance
import main_topo
import obt_infoyam

nombreyaml = '/home/paola/Documentos/app2024/topologia/inventarios/dispositivos.yaml'
datos = obt_infoyam.infyam(nombreyaml)
direc = datos.keys()  # Direcciones IP Filtradas

l, nodb, info_int, ff, fif = main_topo.ejecutar_proceso(direc, datos)
print("Conexiones:", l)
print("Nodos Bloqueados:", nodb)
print("Información de Interfaces:", info_int)

s, dp = loadbalance.ob_yaml(l,nodb,info_int)
loadbalance.yaml_web(dp)
loadbalance.yaml_datos(s)