const { exec } = require('child_process');
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

  /*function balanceo(req, res) {
    if (req.session.loggedin) {
      const pathToPythonScript = '//home/paola/Documentos/app2024/topologia/main_balanceo.py';
      const resPython = execSync(`python3 ${pathToPythonScript}`);
      console.log('Respuesta de Python:', resPython.toString());
      
      const datos = cargarDatos();
      res.render('epops/balanceo', {
        name: req.session.name,
        datos: datos // Pasa los datos a la vista
    });
    } else {
        res.redirect('/');
    }
  }*/
  /*function balanceo(req, res) {
    if (req.session.loggedin) {
      console.log(`ejecutandoooo`);
        // Ejecutar el script de Python antes de cargar los datos
        exec('python3 /home/paola/Documentos/app2024/topologia/main_balanceo.py', (error, stdout, stderr) => {
            if (error) {
                console.error(`Error al ejecutar el script de Python: ${error}`);
                return res.status(500).send('Error al procesar la solicitud de balanceo');
            }
            console.log(`Resultado del script: ${stdout}`);
            const datos = cargarDatos(); // Carga los datos después de ejecutar el script
            res.render('epops/balanceo', {
                name: req.session.name,
                datos: datos
            });
        });
    } else {
        res.redirect('/');
    }
}*/



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
    }