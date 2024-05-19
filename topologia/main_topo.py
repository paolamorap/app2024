import bridge_id
import stp_info
import com_conex
import map_int
import stp_blk
import verstp

def ejecutar_proceso(direc, datos):
    b_id, f1, fif1 = bridge_id.bri_id(direc, datos)
    st_inf, f2, fif2 = stp_info.stp_inf(direc, datos)
    l = com_conex.b_conex(direc, b_id, st_inf)
    info_int, f3, fif3 = map_int.ma_in_complete(direc, datos)
    nf = verstp.obtener_numeros_despues_del_punto(l)
    nodb, f4, fif4 = stp_blk.stp_status(direc, nf, datos)
    return l, nodb, info_int
