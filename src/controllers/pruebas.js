const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

function procesarBalanceo(req, res) {
    const datos = req.body;
    console.log(datos);
    const enlaceName = datos.enlace;

    // Leer el archivo YAML existente
    const filePath = path.join(__dirname, '..', '..', 'topologia', 'balanceo', 'balanceo_datos.yaml');
    const conexionesDisp = yaml.load(fs.readFileSync(filePath, 'utf8'));

    // Leer el archivo YAML de los dispositivos
    const devicesFilePath = path.join(__dirname, '..', '..', 'topologia', 'inventarios','devices.yaml');
    const devicesData = yaml.load(fs.readFileSync(devicesFilePath, 'utf8'));

    // Función para obtener la marca según la IP
    const obtenerMarcaPorIP = (ip) => {
        for (const [marcaKey, data] of Object.entries(devicesData)) {
            for (const host of Object.values(data.hosts)) {
                if (host.host === ip) {
                    return data.vars.marca;
                }
            }
        }
        return 'desconocida';
    };

    // Extraer los datos correspondientes al enlace seleccionado
    const enlaceData = conexionesDisp.conexiones_disp[enlaceName];
    if (!enlaceData) {
        return res.status(400).json({ message: `Enlace ${enlaceName} no encontrado` });
    }

    // Datos del formulario
    const { modoSTP, vlan1, user, password } = datos;

    // Agregar la marca a cada host
    for (const hostKey of Object.keys(enlaceData)) {
        if (hostKey.startsWith('host')) {
            const ip = enlaceData[hostKey].IP;
            const marca = obtenerMarcaPorIP(ip);
            enlaceData[hostKey].marca = marca;
        }
    }

    // Crear el nuevo contenido YAML
    const newYamlData = {
        conexiones_disp: {
            [enlaceName]: {
                ...enlaceData,
                vars: {
                    modoSTP,
                    vlan1,
                    user,
                    password
                }
            }
        }
    };

    // Escribir los datos en un nuevo archivo YAML
    const newFilePath = path.join(__dirname, '..', '..', 'topologia', 'balanceo', 'configuraciones_balanceoprueba.yaml');
    fs.writeFileSync(newFilePath, yaml.dump(newYamlData, { indent: 2, lineWidth: 100 }));

    res.json({ message: "Datos recibidos y procesados correctamente", newYamlData });
}

// Ejemplo de uso
const req = {
    body: {
        enlace: 'enlace1',
        modoSTP: 'mstp',
        vlan1: '2',
        user: 'tets',
        password: 'dsd'
    }
};

const res = {
    json: (data) => console.log(data),
    status: (code) => ({ json: (data) => console.log(`Error ${code}:`, data) })
};

// Llamar a la función con datos de ejemplo
procesarBalanceo(req, res);
