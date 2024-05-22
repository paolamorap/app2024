

var topologyData = {
    "links": [
        {
            "id": 0,
            "index": 1,
            "port_bloks": false,
            "port_blokt": false,
            "source": 1,
            "srcDevice": "192.168.20.2",
            "srcIfName": "G3/0",
            "target": 2,
            "tgtDevice": "192.168.20.3",
            "tgtIfName": "G2/1"
        },
        {
            "id": 1,
            "index": 1,
            "port_bloks": false,
            "port_blokt": false,
            "source": 1,
            "srcDevice": "192.168.20.2",
            "srcIfName": "G0/1",
            "target": 3,
            "tgtDevice": "192.168.20.4",
            "tgtIfName": "G0/3"
        },
        {
            "id": 2,
            "index": 1,
            "port_bloks": false,
            "port_blokt": false,
            "source": 1,
            "srcDevice": "192.168.20.2",
            "srcIfName": "G0/0",
            "target": 4,
            "tgtDevice": "192.168.20.5",
            "tgtIfName": "G0/0"
        },
        {
            "id": 3,
            "index": 1,
            "port_bloks": false,
            "port_blokt": true,
            "source": 2,
            "srcDevice": "192.168.20.3",
            "srcIfName": "G1/0",
            "target": 0,
            "tgtDevice": "192.168.20.10",
            "tgtIfName": "G0/3"
        },
        {
            "id": 4,
            "index": 1,
            "port_bloks": false,
            "port_blokt": false,
            "source": 3,
            "srcDevice": "192.168.20.4",
            "srcIfName": "G1/1",
            "target": 0,
            "tgtDevice": "192.168.20.10",
            "tgtIfName": "G0/1"
        },
        {
            "id": 5,
            "index": 1,
            "port_bloks": false,
            "port_blokt": true,
            "source": 3,
            "srcDevice": "192.168.20.4",
            "srcIfName": "G0/1",
            "target": 2,
            "tgtDevice": "192.168.20.3",
            "tgtIfName": "G0/0"
        },
        {
            "id": 6,
            "index": 2,
            "port_bloks": false,
            "port_blokt": true,
            "source": 3,
            "srcDevice": "192.168.20.4",
            "srcIfName": "G1/0",
            "target": 2,
            "tgtDevice": "192.168.20.3",
            "tgtIfName": "G0/1"
        },
        {
            "id": 7,
            "index": 1,
            "port_bloks": false,
            "port_blokt": true,
            "source": 3,
            "srcDevice": "192.168.20.4",
            "srcIfName": "G0/2",
            "target": 4,
            "tgtDevice": "192.168.20.5",
            "tgtIfName": "G0/1"
        }
    ],
    "nodes": [
        {
            "IP": "192.168.20.10",
            "icon": "switch",
            "id": 0,
            "layerSortPreference": 3,
            "marca": "CISCO",
            "name": "S5"
        },
        {
            "IP": "192.168.20.2",
            "icon": "switch",
            "id": 1,
            "layerSortPreference": 1,
            "marca": "CISCO",
            "name": "S1"
        },
        {
            "IP": "192.168.20.3",
            "icon": "switch",
            "id": 2,
            "layerSortPreference": 2,
            "marca": "CISCO",
            "name": "S2"
        },
        {
            "IP": "192.168.20.4",
            "icon": "switch",
            "id": 3,
            "layerSortPreference": 2,
            "marca": "CISCO",
            "name": "S3"
        },
        {
            "IP": "192.168.20.5",
            "icon": "switch",
            "id": 4,
            "layerSortPreference": 2,
            "marca": "CISCO",
            "name": "S4"
        }
    ]
};