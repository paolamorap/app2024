def get_topology_diff(cached, current):
    """
    Topology diff analyzer and generator.
    Accepts two valid topology dicts as an input.
    Returns:
    - dict with added and deleted nodes,
    - dict with added and deleted links,
    - dict with merged input topologies with extended
      attributes for topology changes visualization
    """
    diff_nodes = {'added': [], 'deleted': []}
    diff_links = {'added': [], 'deleted': []}
    diff_merged_topology = {'nodes': [], 'links': []}
    # Parse links from topology dicts into the following format:
    # (topology_link_obj, (source_hostnme, source_port), (dest_hostname, dest_port))
    cached_links = [(x, ((x['srcDevice'], x['srcIfName']), (x['tgtDevice'], x['tgtIfName']))) for x in cached['links']]
    links = [(x, ((x['srcDevice'], x['srcIfName']), (x['tgtDevice'], x['tgtIfName']))) for x in current['links']]
    # Parse nodes from topology dicts into the following format:
    # (topology_node_obj, (hostname,))
    # Some additional values might be added for comparison later on to the tuple above.
    cached_nodes = [(x, (x['name'],)) for x in cached['nodes']]
    nodes = [(x, (x['name'],)) for x in current['nodes']]
    # Search for deleted and added hostnames.
    node_id = 0
    host_id_map = {}
    for raw_data, node in nodes:
        if node in [x[1] for x in cached_nodes]:
            raw_data['id'] = node_id
            host_id_map[raw_data['name']] = node_id
            raw_data['is_new'] = 'no'
            raw_data['is_dead'] = 'no'
            diff_merged_topology['nodes'].append(raw_data)
            node_id += 1
            continue
        diff_nodes['added'].append(node)
        raw_data['id'] = node_id
        host_id_map[raw_data['name']] = node_id
        raw_data['is_new'] = 'yes'
        raw_data['is_dead'] = 'no'
        diff_merged_topology['nodes'].append(raw_data)
        node_id += 1
    for raw_data, cached_node in cached_nodes:
        if cached_node in [x[1] for x in nodes]:
            continue
        diff_nodes['deleted'].append(cached_node)
        raw_data['id'] = node_id
        host_id_map[raw_data['name']] = node_id
        raw_data['is_new'] = 'no'
        raw_data['is_dead'] = 'yes'
        raw_data['icon'] = 'dead_node'
        diff_merged_topology['nodes'].append(raw_data)
        node_id += 1
    # Search for deleted and added interconnections.
    # Interface change on some side is considered as
    # one interconnection deletion and one interconnection insertion.
    # Check for permutations as well:
    # ((h1, Gi1), (h2, Gi2)) and ((h2, Gi2), (h1, Gi1)) are equal.
    link_id = 0
    for raw_data, link in links:
        src, dst = link
        if not (src, dst) in [x[1] for x in cached_links] and not (dst, src) in [x[1] for x in cached_links]:
            diff_links['added'].append((src, dst))
            raw_data['id'] = link_id
            link_id += 1
            raw_data['source'] = host_id_map[src[0]]
            raw_data['target'] = host_id_map[dst[0]]
            raw_data['is_new'] = 'yes'
            raw_data['is_dead'] = 'no'
            diff_merged_topology['links'].append(raw_data)
            continue
        raw_data['id'] = link_id
        link_id += 1
        raw_data['source'] = host_id_map[src[0]]
        raw_data['target'] = host_id_map[dst[0]]
        raw_data['is_new'] = 'no'
        raw_data['is_dead'] = 'no'
        diff_merged_topology['links'].append(raw_data)
    for raw_data, link in cached_links:
        src, dst = link
        if not (src, dst) in [x[1] for x in links] and not (dst, src) in [x[1] for x in links]:
            diff_links['deleted'].append((src, dst))
            raw_data['id'] = link_id
            link_id += 1
            raw_data['source'] = host_id_map[src[0]]
            raw_data['target'] = host_id_map[dst[0]]
            raw_data['is_new'] = 'no'
            raw_data['is_dead'] = 'yes'
            diff_merged_topology['links'].append(raw_data)
    return diff_nodes, diff_links, diff_merged_topology


cached = {
    'nodes': [{'name': 'Switch1'}, {'name': 'Router1'}],
    'links': [{'srcDevice': 'Switch1', 'srcIfName': 'Gi0', 'tgtDevice': 'Router1', 'tgtIfName': 'Gi1'}]
}
current = {
    'nodes': [{'name': 'Switch1'}, {'name': 'Router2'}],
    'links': [{'srcDevice': 'Switch1', 'srcIfName': 'Gi0', 'tgtDevice': 'Router2', 'tgtIfName': 'Gi2'}]
}

diff_nodes, diff_links, diff_merged_topology = get_topology_diff(cached, current)

print("Nodos añadidos:", diff_nodes)
#print("Nodos eliminados:", diff_nodes)
print("Enlaces añadidos:", diff_links)
#print("Enlaces eliminados:", diff_links)
print("\n")
print(diff_merged_topology )

