def id_red(con):
    # Crear una nueva lista para almacenar las conexiones modificadas
    conm = []
    # Iterar sobre cada tupla de conexiones
    for tupla in con:
        # Crear una nueva tupla con las direcciones IP modificadas
        tupla_modificada = tuple(direccion.split("-")[0] for direccion in tupla)
        conm.append(tupla_modificada)

    # Convertir cada tupla en un conjunto para ignorar el orden
    lista = [sorted(tupla) for tupla in conm]
    conexredun  = {}
    conexredu1  = {}

    for i in lista:
        a = lista.count(i)
        if a >= 2:
           conexredun[str(i)] = ""
        if a <= 1:
           conexredu1[str(i)] = ""


    return list(conexredun.keys()),list(conexredu1.keys())