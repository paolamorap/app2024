def hex_to_decimal(hex_string):
    decimal = int(hex_string, 16)
    return str(decimal)

def b_conex(direc,b_id,stp_in):
    lc = []
    for i in direc:
        ini = i
        for j in direc:
            c = 0
            inf = stp_in[j]
            inj = j
            for p in range(len(inf[0])):
                try:
                    if b_id[i] == inf[0][p] and i!=j:
                        c_j = inf[1][c][0]
                        c_i = inf[1][c][1]
                        lc.append((ini+"-"+hex_to_decimal(c_i[-2:]),inj+"-"+c_j))
                    c += 1
                except KeyError:
                    pass
    return lc


