from textwrap import dedent

def comandos_snmp(comunidad):
    """
    Genera un archivo de texto con comandos de configuración para SNMP.

    Parámetros:
        comunidad (str): El nombre de laa comunidad SNMP.
    """
    # Preparar los comandos con los valores proporcionados
    nombre_archivo = '/home/du/Auto_Mon_2024_Cod/Automatizacion_Red_2024/epops/comandos/comandos_snmp.txt'
    comandos = dedent(f"""
    configure
    snmp-server community {comunidad} read-only
    """)

    # Escribir los comandos en el archivo
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(comandos.strip())

    return nombre_archivo

def comandos_stp(region):
    """
    Genera un archivo de texto con comandos de configuración para MSTP.

    Parámetros:
        region (str): El nombre de la region MSTP.
    """
    nombre_archivo = '/home/du/Auto_Mon_2024_Cod/Automatizacion_Red_2024/epops/comandos/comandos_stp.txt'
    # Preparar los comandos con los valores proporcionados
    comandos = dedent(f"""
    configure
    spanning-tree mode mst
    spanning-tree extend system-id
    spanning-tree mst configuration
    name {region}
    """)

    # Escribir los comandos en el archivo
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(comandos.strip())
    return nombre_archivo