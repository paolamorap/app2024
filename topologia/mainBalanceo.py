import loadBalanceo
import datos_balanceo
import obt_infyam
import sys
import os

def main():
    try:
        current_dir = os.path.dirname(__file__)
        archivoDispositivos = os.path.join(current_dir, 'inventarios', 'dispositivos.yaml')
        datos = obt_infyam.infyam(archivoDispositivos)
        direc = datos.keys()  # Direcciones IP Filtradas
        l, nodb, info_int = datos_balanceo.ejecutar_proceso(direc, datos)
        s, dp = loadBalanceo.ob_yaml(l, nodb, info_int)
        loadBalanceo.yaml_web(dp)
        loadBalanceo.yaml_datos(s)
        print("Script ejecutado correctamente")
        
    except Exception as e:
        print(f"Error al ejecutar el script: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()