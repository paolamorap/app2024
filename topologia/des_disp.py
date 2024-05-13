import ipaddress
import subprocess



def check_device_availability(ip):
    try:
        # Ejecutar el comando ping con un timeout de 2 segundos
        subprocess.run(["ping", "-c", "1", "-W", "2", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    

def listar_hosts_subred(subred, mascara):
    # Convertir la dirección de subred y la máscara en un objeto de red IPv4
    red = ipaddress.ip_network(f"{subred}/{mascara}", strict=False)
    d = []
    # Iterar sobre todos los hosts en la red e imprimirlos
    for host in red.hosts():
        if check_device_availability(str(host)):
            d.append(str(host))

    return d
def listar_hosts_rango_con_mascara(inicio, fin, mascara):
    d = []
    # Convertir las direcciones IP de inicio y fin en objetos IP
    ip_inicio = ipaddress.ip_address(inicio)
    ip_fin = ipaddress.ip_address(fin)
    
    # Obtener la red común basada en las direcciones IP proporcionadas y la máscara de subred
    red = ipaddress.ip_network(f"{inicio}/{mascara}", strict=False)
    
    # Iterar sobre todos los hosts en la red común e imprimirlos
    for host in red.hosts():
        if host >= ip_inicio and host <= ip_fin:
            if check_device_availability(str(host)):
                        d.append(str(host))

    return d 


def in_des():
    print("Ingresar el Modo de Descubrimiento")
    print("Ingrese 1 para ingresar una subred")
    print("Ingrese 2 para ingresar un rango de direcciones")
    m = int(input("Modo: "))
    if m == 1:
        subred = input("Ingrese la dirección de subred (ejemplo: 192.168.1.0): ")
        mascara = input("Ingrese la dirección de subred (ejemplo: 24): ")
        l = listar_hosts_subred(subred, mascara)
    else:
        inicio = input("Ingrese la dirección IP de inicio del rango: ")
        fin = input("Ingrese la dirección IP de inicio del rango: ")
        mascara = input("Ingrese la dirección de subred (ejemplo: 24): ")
        l = listar_hosts_rango_con_mascara(inicio, fin, mascara)
    return l
