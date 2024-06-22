def tplink_id(b_root, data_stp ,br_idtp,iptp):
    """
    Permite intercambiar los datos del diccionario con la información de STP
    para todos los dispositivos TpLink.

    Parameters:
    b_root(str):     ID del BridgeRoot(Necesario puesto que se intercambiara por un nuevo BridgeID)
    data_stp(di):    Información de STP de todos los switches
    br_idtp():       Bridge ID real del dispositivo TP_Link
    iptp(list):      Direcciones IP de dispositivos TpLink  
    
    Return:
    dp(dict):        Nueva información de STP con los datos de los switches TpLink Corregidos

    """
    for i in iptp:
        if i in br_idtp.keys():
            try:
               i_c = data_stp[i][0].index(b_root)
               data_stp[i][0][i_c] = br_idtp[i]
            except ValueError as e:
               print(f"Error: {e}")
        else:
            try:
               i_c = data_stp[i][0].index(b_root)
               data_stp[i][0][i_c] = "11111111"
            except ValueError as e:
               print(f"Error: {e}")
    return data_stp