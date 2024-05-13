const { exec } = require('child_process');

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

/*function run_script(req, res) {
  if (req.session.loggedin) {
      // Usar la ruta absoluta del script
      const scriptPath = '/home/paola/Documentos/loginapp/src/configure/epolaris_install.sh';
      
      exec(`bash ${scriptPath}`, (error, stdout, stderr) => {
          if (error) {
              console.error(`error: ${stderr}`);
              return res.status(500).json({ success: false, message: 'Error al ejecutar el script', error: stderr });
          }
          console.log(`stdout: ${stdout}`);
          res.json({ success: true, message: 'Script ejecutado correctamente', output: stdout });
      });
  } else {
      res.redirect('/');
      res.status(403).json({ success: false, message: 'No autorizado' });
  }
}*/


function run_script(req, res) {
  // Verificar si el usuario está logueado
  if (!req.session.loggedin) {
      // Redirigir y terminar la ejecución inmediatamente después
      return res.redirect('/');
  }

  // Definir la ruta del script
  const scriptPath = '/home/paola/Documentos/loginapp/src/configure/epolaris_install.sh';
  
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
    }