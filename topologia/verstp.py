def obtener_numeros_despues_del_punto(conexiones):
    """
    Crea un diccionario donde las claves son los dígitos antes del punto y los valores son listas
    que contienen los números que siguen después del punto en las tuplas de conexiones.

    Args:
    - conexiones (list): Lista de tuplas que representan las conexiones entre nodos.

    Returns:
    - dict: Diccionario donde las claves son los dígitos antes del punto y los valores son listas
            que contienen los números que siguen después del punto en las tuplas de conexiones.
    """
    numeros_despues_del_punto = {}
    for tupla in conexiones:
        # Para el primer elemento de la tupla
        clave = tupla[0].split('-')[0]
        numero_despues_del_punto = tupla[0].split('-')[1]
        if clave in numeros_despues_del_punto:
            numeros_despues_del_punto[clave].append(numero_despues_del_punto)
        else:
            numeros_despues_del_punto[clave] = [numero_despues_del_punto]

        # Para el segundo elemento de la tupla
        clave = tupla[1].split('-')[0]
        numero_despues_del_punto = tupla[1].split('-')[1]
        if clave in numeros_despues_del_punto:
            numeros_despues_del_punto[clave].append(numero_despues_del_punto)
        else:
            numeros_despues_del_punto[clave] = [numero_despues_del_punto]

    return numeros_despues_del_punto
