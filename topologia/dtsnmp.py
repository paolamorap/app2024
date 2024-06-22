def snmt(*lists):
    """
    Permite unir listas dentro de listas en un solo diccionario que guarda elementos unicos

    Parameters:
    lists(list):    Lista

    Return:
    sal(dict):      Diccionario con elementos unicos de las entradas
    """
    sal = {}
    for lst in lists:
        for key in lst:
            sal[key] = ""
    return sal