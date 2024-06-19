

var topologyData = {
    "links": [
        {
            "id": 0,
            "index": 1,
            "port_bloks": false,
            "port_blokt": false,
            "source": 0,
            "srcDevice": "192.168.122.2",
            "srcIfName": "G0/3",
            "target": 1,
            "tgtDevice": "192.168.122.3",
            "tgtIfName": "G0/3"
        },
        {
            "id": 1,
            "index": 1,
            "port_bloks": false,
            "port_blokt": false,
            "source": 0,
            "srcDevice": "192.168.122.2",
            "srcIfName": "G0/2",
            "target": 2,
            "tgtDevice": "192.168.122.4",
            "tgtIfName": "G0/0"
        },
        {
            "id": 2,
            "index": 1,
            "port_bloks": false,
            "port_blokt": false,
            "source": 1,
            "srcDevice": "192.168.122.3",
            "srcIfName": "G1/0",
            "target": 3,
            "tgtDevice": "192.168.122.5",
            "tgtIfName": "G0/1"
        },
        {
            "id": 3,
            "index": 2,
            "port_bloks": false,
            "port_blokt": true,
            "source": 1,
            "srcDevice": "192.168.122.3",
            "srcIfName": "G1/1",
            "target": 3,
            "tgtDevice": "192.168.122.5",
            "tgtIfName": "G0/2"
        },
        {
            "id": 4,
            "index": 1,
            "port_bloks": false,
            "port_blokt": true,
            "source": 2,
            "srcDevice": "192.168.122.4",
            "srcIfName": "G0/1",
            "target": 1,
            "tgtDevice": "192.168.122.3",
            "tgtIfName": "G0/2"
        },
        {
            "id": 5,
            "index": 1,
            "port_bloks": false,
            "port_blokt": false,
            "source": 2,
            "srcDevice": "192.168.122.4",
            "srcIfName": "G0/2",
            "target": 4,
            "tgtDevice": "192.168.122.6",
            "tgtIfName": "G0/1"
        },
        {
            "id": 6,
            "index": 1,
            "port_bloks": false,
            "port_blokt": false,
            "source": 3,
            "srcDevice": "192.168.122.5",
            "srcIfName": "G0/3",
            "target": 5,
            "tgtDevice": "192.168.122.7",
            "tgtIfName": "G0/1"
        }
    ],
    "nodes": [
        {
            "IP": "192.168.122.2",
            "icon": "switch",
            "id": 0,
            "layerSortPreference": 1,
            "marca": "CISCO",
            "name": "S1_Cuenca"
        },
        {
            "IP": "192.168.122.3",
            "icon": "switch",
            "id": 1,
            "layerSortPreference": 2,
            "marca": "CISCO",
            "name": "S2_Totoracocha"
        },
        {
            "IP": "192.168.122.4",
            "icon": "switch",
            "id": 2,
            "layerSortPreference": 2,
            "marca": "CISCO",
            "name": "S3_Ricaurte"
        },
        {
            "IP": "192.168.122.5",
            "icon": "switch",
            "id": 3,
            "layerSortPreference": 3,
            "marca": "CISCO",
            "name": "S4_UCuenca"
        },
        {
            "IP": "192.168.122.6",
            "icon": "switch",
            "id": 4,
            "layerSortPreference": 3,
            "marca": "CISCO",
            "name": "S5_Bibin"
        },
        {
            "IP": "192.168.122.7",
            "icon": "switch",
            "id": 5,
            "layerSortPreference": 4,
            "marca": "CISCO",
            "name": "S6_Valle"
        }
    ]
};