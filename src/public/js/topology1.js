

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
            "srcIfName": "G0/1",
            "target": 3,
            "tgtDevice": "192.168.122.5",
            "tgtIfName": "G0/0"
        },
        {
            "id": 3,
            "index": 1,
            "port_bloks": false,
            "port_blokt": true,
            "source": 2,
            "srcDevice": "192.168.122.4",
            "srcIfName": "G0/1",
            "target": 1,
            "tgtDevice": "192.168.122.3",
            "tgtIfName": "G0/2"
        }
    ],
    "nodes": [
        {
            "IP": "192.168.122.2",
            "icon": "switch",
            "id": 0,
            "layerSortPreference": 1,
            "marca": "CISCO",
            "name": "S1"
        },
        {
            "IP": "192.168.122.3",
            "icon": "switch",
            "id": 1,
            "layerSortPreference": 2,
            "marca": "CISCO",
            "name": "S2"
        },
        {
            "IP": "192.168.122.4",
            "icon": "switch",
            "id": 2,
            "layerSortPreference": 2,
            "marca": "CISCO",
            "name": "S3"
        },
        {
            "IP": "192.168.122.5",
            "icon": "switch",
            "id": 3,
            "layerSortPreference": 3,
            "marca": "CISCO",
            "name": "S4"
        },
        {
            "IP": "192.168.122.6",
            "icon": "switch",
            "id": 4,
            "layerSortPreference": 0,
            "marca": "CISCO",
            "name": "None"
        }
    ]
};