def info_proactivo():

    with open('datos.txt', 'r') as archivo:
        direc = eval(archivo.readline().strip())
        l = eval(archivo.readline().strip())
        interconexiones = eval(archivo.readline().strip())
        bridge_root = eval(archivo.readline().strip())

    return direc,l,interconexiones,bridge_root