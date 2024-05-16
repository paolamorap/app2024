const { exec, execSync } = require('child_process');
const path = require('path');
var fs = require('fs');
const yaml = require('js-yaml');


function snmp(req, res) {
    if (req.session.loggedin ){
      res.render('epops/snmp', {name: req.session.name});
    }else{
      res.redirect('/');
    }
  }

function stp(req, res) {
    if (req.session.loggedin ){
      res.render('epops/stp', {name: req.session.name});
    }else{
      res.redirect('/');
    }
  }

  function stp1(req, res) {
    if (req.session.loggedin ){
      res.render('epops/stp1', {name: req.session.name});
    }else{
      res.redirect('/');
    }
  }

  function pathcost(req, res) {
    if (req.session.loggedin ){
      res.render('epops/pathcost', {name: req.session.name});
    }else{
      res.redirect('/');
    }
  }

  function vlan(req, res) {
    if (req.session.loggedin ){
      res.render('epops/vlan', {name: req.session.name});
    }else{
      res.redirect('/');
    }
  }

  function logs(req, res) {
    if (req.session.loggedin ){
      res.render('epops/logs', {name: req.session.name});
    }else{
      res.redirect('/');
    }
  }

  function access_list(req, res) {
    if (req.session.loggedin ){
      res.render('epops/access_list', {name: req.session.name});
    }else{
      res.redirect('/');
    }
  }

  function start_app(req, res) {
    if (req.session.loggedin) {
        res.render('epops/start_app', { name: req.session.name });
    } else {
        res.redirect('/');
    }
  }

  function cargarDatos() {
    try {
        const filePath = path.join(__dirname, '../../topologia/balanceo/balanceo_web.yaml');
        const fileContents = fs.readFileSync(filePath, 'utf8');
        return yaml.load(fileContents);
    } catch (e) {
        console.error(e);
        return {};
    }
  }

  function balanceo(req, res) {
    if (req.session.loggedin) {
      const datos = cargarDatos();
      res.render('epops/balanceo', {
        name: req.session.name,
        datos: datos // Pasa los datos a la vista
    });
    } else {
        res.redirect('/');
    }
  }

  function cargarArchivo(req, res) {
    if (!req.session.loggedin) {
      return res.redirect('/');
    }
  
    const pathToPythonScript = '/home/paola/Documentos/app2024/topologia/main_balanceo.py';
    console.log(`Ejecutando script: ${pathToPythonScript}`);
    exec(`python3 ${pathToPythonScript}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error al ejecutar el script: ${stderr}`);
        return res.status(500).json({ success: false, message: 'Error al ejecutar el script', error: stderr });
      }
      
      if (!req.session.loggedin) {
        console.error('La sesión ha expirado antes de completar el script');
        return res.status(403).json({ success: false, message: 'Sesión expirada' });
      }
  
      console.log(`Script ejecutado correctamente: ${stdout}`);
      res.json({ success: true, message: 'Script ejecutado correctamente', output: stdout });
    });
  }
  
  /*function procesarBalanceo(req, res){
    const datos = req.body;
    // Aquí puedes procesar los datos recibidos
    console.log("Datos recibidos:", datos);
    enlace_name = datos.enlace 


    res.json({ message: "Datos recibidos y procesados correctamente" });
  }*/

  function procesarBalanceo(req, res) {
    const datos = req.body;
    console.log(datos)
    const enlaceName = datos.enlace;

    // Leer el archivo YAML existente
    const filePath = path.join(__dirname, '..','..','topologia', 'balanceo', 'balanceo_datos.yaml');
    const conexionesDisp = yaml.load(fs.readFileSync(filePath, 'utf8'));

    // Extraer los datos correspondientes al enlace seleccionado
    const enlaceData = conexionesDisp.conexiones_disp[enlaceName];
    if (!enlaceData) {
        return res.status(400).json({ message: `Enlace ${enlaceName} no encontrado` });
    }

    // Datos del formulario
    const { modoSTP, vlan1, user, password } = datos;

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
    const newFilePath = path.join(__dirname, '..','..','topologia', 'balanceo', 'configuraciones_balanceo.yaml');
    fs.writeFileSync(newFilePath, yaml.dump(newYamlData, { indent: 2, lineWidth: 100 }));

    res.json({ message: "Datos recibidos y procesados correctamente", newYamlData });
}
    
function run_script(req, res) {
  // Verificar si el usuario está logueado
  if (!req.session.loggedin) {
      // Redirigir y terminar la ejecución inmediatamente después
      return res.redirect('/');
  }

  // Definir la ruta del script
  const scriptPath = '/home/paola/Documentos/app2024/src/configure/epolaris_install.sh';
  
  // Ejecutar el script
  exec(`bash ${scriptPath}`, (error, stdout, stderr) => {
      if (error) {
          console.error(`Error al ejecutar el script: ${stderr}`);
          return res.status(500).json({ success: false, message: 'Error al ejecutar el script', error: stderr });
      }
      
      // Comprobar de nuevo el estado de la sesión antes de enviar la respuesta
      if (!req.session.loggedin) {
          console.error('La sesión ha expirado antes de completar el script');
          return res.status(403).json({ success: false, message: 'Sesión expirada' });
      }

      console.log(`Script ejecutado correctamente: ${stdout}`);
      res.json({ success: true, message: 'Script ejecutado correctamente', output: stdout });
  });
}



  
    module.exports = {
      snmp: snmp,
      stp:stp,
      vlan:vlan,
      stp1:stp1,
      logs:logs,
      access_list:access_list,
      start_app: start_app,
      run_script: run_script,
      pathcost: pathcost,
      balanceo: balanceo,
      cargarArchivo: cargarArchivo,
      procesarBalanceo: procesarBalanceo,
    }