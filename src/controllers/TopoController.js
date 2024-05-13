function topo_ini(req, res) {
  if (req.session.loggedin ){
    res.render('epops/topo', {name: req.session.name});
  }else{
    res.redirect('/');
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
    operaciones_ini: operaciones_ini,
  }