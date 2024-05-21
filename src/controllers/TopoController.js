const path = require('path');
const fs = require('fs');

function topo_ini(req, res) {
  if (req.session.loggedin ){
    res.render('epops/topo', {name: req.session.name});
  }else{
    res.redirect('/');
  }
}

function topo_inicial(req, res) {
  if (req.session.loggedin) {
    // Chequear si hay cambios
    const change = req.session.change || false;  // Asume que almacenamos el estado de cambio en la sesión

    console.log('CAMBIO', change)

    if (change) {
      res.render('epops/topologia_diff', {name: req.session.name});
    } else {
      res.render('epops/topologia', {name: req.session.name});
    }
  } else {
    res.redirect('/');
  }
}


function update_Topology(req, res) {
  console.log('Antes de actualizar la sesión:', req.session.change);
  if (req.session.loggedin) {
    const filePath = path.join(__dirname, '..', 'public', 'js', 'changes_flag.json');
    // Asegúrate de actualizar el estado y escribir en el archivo antes de redirigir
    req.session.change = false; // Actualiza el estado de 'change' a false
    try {
      fs.writeFileSync(filePath, JSON.stringify({ changes: false }));
      
      console.log('Después de actualizar la sesión:', req.session.change);
      res.render('epops/topologia', {name: req.session.name});
    } catch (error) {
      console.error('Error al escribir en changes_flag.json:', error);
      res.status(500).send('Error interno del servidor al confirmar los cambios');
    }
  } else {
    res.redirect('/'); // Si no está logueado, redirige a la página de inicio
  }
}

function verificarCambios() {
  const filePath = path.join(__dirname, '..', 'public', 'js', 'changes_flag.json');
  const data = fs.readFileSync(filePath);
  const result = JSON.parse(data);
  return result.changes;
}


function chageDetect(req, res){
  if (req.session.loggedin) {
    req.session.change = verificarCambios(); // Actualiza la sesión con el valor del archivo
    topo_inicial(req, res); // Llama a la función que decide qué vista mostrar
  } else {
    res.redirect('/');
  }
}

function checkChange(req, res){
  if (req.session.loggedin) {
    req.session.change = verificarCambios()
    console.log('cambio regustrado para actualizar',req.session.change)
    res.json({change: req.session.change})
  } else {
    res.status(401).json({error: 'NO AUTORIZADO'})
  }
}


function operaciones_ini(req, res) {
  if (req.session.loggedin ){
    res.render('epops/operaciones', {name: req.session.name});
  }else{
    res.redirect('/');
  }
}

  module.exports = {
    topo_ini: topo_ini,
    topo_inicial: topo_inicial,
    operaciones_ini: operaciones_ini,
    update_Topology: update_Topology,
    chageDetect: chageDetect,
    checkChange: checkChange,
  }


  