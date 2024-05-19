import loadbalance
import main_topo
import obt_infoyam
import sys

def main():
    try:
        nombreyaml = '/home/paola/Documentos/app2024/topologia/inventarios/dispositivos.yaml'
        datos = obt_infoyam.infyam(nombreyaml)
        direc = datos.keys()  # Direcciones IP Filtradas
    
        l, nodb, info_int = main_topo.ejecutar_proceso(direc, datos)
        s, dp = loadbalance.ob_yaml(l, nodb, info_int)
        loadbalance.yaml_web(dp)
        loadbalance.yaml_datos(s)
        print("Script ejecutado correctamente")
        
    except Exception as e:
        print(f"Error al ejecutar el script: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
