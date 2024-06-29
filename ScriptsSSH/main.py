import graphic_topology_tree
import tree_network_connection
import time

def main():
    
    username = 'test'
    password = 'test'
    ip_list = ['192.168.122.2', '192.168.122.3', '192.168.122.4', '192.168.122.5', '192.168.122.6']
    inicio1 = time.time()
    device_data, neighbor_device_data, blocked_ports_current_device = tree_network_connection.general_data_device(username, password, ip_list)
    tiempo1=time.time() - inicio1
    print('TIEMPO RECOLECCION DE DATOS: ', tiempo1)

    #device_data, neighbor_device_data, blocked_ports_current_device = tree_network_connection.general_data_device1(username, password)
    #print(device_data)
    #print('--------------------------------')
    #print(neighbor_device_data)
    #print('--------------------------------')
    #print(blocked_ports_current_device)
    inicio2 = time.time()
    device_connections, int_device_connections = tree_network_connection.identify_connections(device_data, neighbor_device_data)
    tiempo2=time.time() - inicio2
    print('TIEMPO IDENTIFICACION DE CONEXIONES: ', tiempo2)

    ##### GRAFICA SIN PUERTOS #####
    graphic_topology_tree.device_connection(device_connections)
    #### GRAFICA CON PUERTOS ####
    graphic_topology_tree.device_connection_interfaces_block(int_device_connections,blocked_ports_current_device)


if __name__ == "__main__":
    main()
