def generate_link_key(source, target):
    # Ordena los nodos para evitar duplicidad en la dirección del enlace
    return tuple(sorted([source, target]))

def analyze_topology_changes(current_topology, previous_topology):
    current_links = {generate_link_key(link['srcDevice'], link['tgtDevice']): link for link in current_topology['links']}
    previous_links = {generate_link_key(link['srcDevice'], link['tgtDevice']): link for link in previous_topology['links']}

    added = {k: v for k, v in current_links.items() if k not in previous_links}
    removed = {k: v for k, v in previous_links.items() if k not in current_links}
    changed = {k: current_links[k] for k in current_links if k in previous_links and current_links[k] != previous_links[k]}

    return added, removed, changed

# Simular datos de topología anterior y actual
previous_topology = {
    "links": [
        {"srcDevice": "192.168.1.1", "tgtDevice": "192.168.1.2"},
        {"srcDevice": "192.168.1.2", "tgtDevice": "192.168.1.3"}
    ]
}

current_topology = {
    "links": [
        {"srcDevice": "192.168.1.1", "tgtDevice": "192.168.1.2"},  # Sin cambios
        {"srcDevice": "192.168.1.2", "tgtDevice": "192.168.1.4"}   # Cambiado de .3 a .4
    ]
}

added, removed, changed = analyze_topology_changes(current_topology, previous_topology)

print("Added Links:", added)
print("Removed Links:", removed)
print("Changed Links:", changed)
