import networkx as nx
import matplotlib.pyplot as plt
def device_connection(conexiones):
    # Crea un nuevo grafo no dirigido
    G = nx.Graph()
    # Agrega nodos al grafo
    dispositivos = conexiones.keys()
    G.add_nodes_from(dispositivos)
    # Crea una nueva figura de matplotlib
    plt.figure()
    # Agrega bordes (conexiones) al grafo
    for dispositivo, vecinos in conexiones.items():
        for vecino in vecinos:
            G.add_edge(dispositivo, vecino)

    # Dibuja el grafo
    nx.draw(G, with_labels=True)
    # Guarda la figura en un archivo
    plt.savefig("Topologia0.png")

def device_connection_interfaces(salida_final):
    # Crear un nuevo grafo
    G = nx.Graph()
    # Diccionario para mapear nombres de interfaz a identificadores únicos
    interfaz_ids = {}
    # Agregar nodos (dispositivos e interfaces) al grafo
    for (dispositivo, interfaz), (vecino, vecino_interfaz) in salida_final.items():
        # Generar identificadores únicos para las interfaces
        interfaz_id = hash((dispositivo, interfaz))
        vecino_interfaz_id = hash((vecino, vecino_interfaz))
        # Mapear los nombres de interfaz a sus identificadores únicos
        if (dispositivo, interfaz) not in interfaz_ids:
            interfaz_ids[(dispositivo, interfaz)] = interfaz_id
        if (vecino, vecino_interfaz) not in interfaz_ids:
            interfaz_ids[(vecino, vecino_interfaz)] = vecino_interfaz_id

        # Agregar nodos al grafo
        G.add_node(interfaz_id, label=interfaz, node_type='interfaz')
        G.add_node(vecino_interfaz_id, label=vecino_interfaz, node_type='interfaz')
        G.add_node(dispositivo, label=dispositivo, node_type='ip')
        G.add_node(vecino, label=vecino, node_type='ip')

        # Agregar conexiones entre dispositivos e interfaces
        G.add_edge(dispositivo, interfaz_id)
        G.add_edge(interfaz_id, vecino_interfaz_id)
        G.add_edge(vecino_interfaz_id, vecino)

    # Crea una nueva figura de matplotlib
    plt.figure()
    # Dibujar el grafo
    pos = nx.spring_layout(G)
    # Definir colores para los nodos
    node_colors = ['blue' if data['node_type'] == 'ip' else 'orange' for node, data in G.nodes(data=True)]
    nx.draw(G, pos, with_labels=True, labels={node: data['label'] for node, data in G.nodes(data=True)},
            node_color=node_colors)
    nx.draw_networkx_edges(G, pos)
    # Guardar el grafo como imagen
    plt.axis('off')
    plt.savefig("grafo2.png")

def device_connection_interfaces_block(salida_final, puertos_bloqueados):
    # Crear un nuevo grafo
    G = nx.Graph()
    # Diccionario para mapear nombres de interfaz a identificadores únicos
    interfaz_ids = {}

    # Agregar nodos (dispositivos e interfaces) al grafo
    for (dispositivo, interfaz), (vecino, vecino_interfaz) in salida_final.items():
        # Generar identificadores únicos para las interfaces
        interfaz_id = hash((dispositivo, interfaz))
        vecino_interfaz_id = hash((vecino, vecino_interfaz))
        # Mapear los nombres de interfaz a sus identificadores únicos
        if (dispositivo, interfaz) not in interfaz_ids:
            interfaz_ids[(dispositivo, interfaz)] = interfaz_id
        if (vecino, vecino_interfaz) not in interfaz_ids:
            interfaz_ids[(vecino, vecino_interfaz)] = vecino_interfaz_id

        # Agregar nodos al grafo
        G.add_node(interfaz_id, label=interfaz, node_type='interfaz')
        G.add_node(vecino_interfaz_id, label=vecino_interfaz, node_type='interfaz')
        G.add_node(dispositivo, label=dispositivo, node_type='ip')
        G.add_node(vecino, label=vecino, node_type='ip')

        # Agregar conexiones entre dispositivos e interfaces
        G.add_edge(dispositivo, interfaz_id)
        G.add_edge(interfaz_id, vecino_interfaz_id)
        G.add_edge(vecino_interfaz_id, vecino)

    # Crea una nueva figura de matplotlib
    plt.figure()
    # Dibujar el grafo
    pos = nx.spring_layout(G)

    # Definir colores para los nodos
    node_colors = ['blue' if data['node_type'] == 'ip' else 'orange' for node, data in G.nodes(data=True)]
    nx.draw(G, pos, with_labels=True, labels={node: data['label'] for node, data in G.nodes(data=True)},
            node_color=node_colors)

    # Colorear los puertos bloqueados de manera diferente
    blocked_ports = puertos_bloqueados.values()
    for device_ports in blocked_ports:
        for port in device_ports:
            for node, data in G.nodes(data=True):
                if data['node_type'] == 'interfaz' and data['label'] == port:
                    nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='red', node_size=400)

    nx.draw_networkx_edges(G, pos)

    # Guardar el grafo como imagen
    plt.axis('off')
    plt.savefig("Topologia1.png")