import bridge_id
import stp_info
import com_conex
import map_int
import stp_blk
import verstp
import time 
import tree
import obt_infoyam
import dtsnmp
import bridge_id_root
import loadbalance



def ejecutar_proceso(direc, datos):
    b_id, f1, fif1 = bridge_id.bri_id(direc, datos)
    st_inf, f2, fif2 = stp_info.stp_inf(direc, datos)
    f = f1 or f2
    fif = dtsnmp.snmt(fif1, fif2)
    l = com_conex.b_conex(direc, b_id, st_inf)
    info_int, f3, fif3 = map_int.ma_int(direc, datos)
    nf = verstp.obtener_numeros_despues_del_punto(l)
    nodb, f4, fif4 = stp_blk.stp_status(direc, nf, datos)
    ff = f1 or f2 or f3 or f4
    fif = dtsnmp.snmt(fif1, fif2, fif3, fif4)
    return l, nodb, info_int, ff, fif


