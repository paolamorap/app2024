const multer = require('multer');
const yaml = require('js-yaml');
const path = require('path');
const fs = require('fs');
const {existsSync, execSync} = require('child_process')



// Configuración de Multer para archivos YAML
const storageYAML = multer.diskStorage({
  destination: function(req, file, cb) {
      // Especificar la ruta deseada
      const destPath = path.join(__dirname, '..', '..', 'topologia', 'inventarios');
      // Asegurarse de que el directorio existe, si no, crearlo
      fs.mkdirSync(destPath, { recursive: true });
      cb(null, destPath);
  },
  filename: function(req, file, cb) {
      // Usar una combinación de marca de tiempo y el nombre original del archivo
      const newName = "dispositivos1" + path.extname(file.originalname); // Asegúrate de añadir la extensión
      cb(null, newName);
  }
});

const uploadYAML = multer({ storage: storageYAML });

function uploadYAMLFile(req, res) {
  console.log(req.file);  // Log para ver la información del archivo cargado
  if (!req.file) {
    return res.status(400).send('No se subió ningún archivo.');
  }
  res.json({ message: 'Archivo YAML subido con éxito!' });
}

function configure_archivo(req, res) {
  if (req.session.loggedin ){
    res.render('epops/archivoyaml', {name: req.session.name});
  }else{
    res.redirect('/');
  }
      
}

function configure_ini(req, res) {
  if (req.session.loggedin ){
    res.render('epops/datos', {name: req.session.name});
  }else{
    res.redirect('/');
  }
      
}
  
function esIPValida(ip) {
  const regexIP = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
  return regexIP.test(ip);
}

function esTipoDispositivoValido(tipo) {
  const tiposValidos = ['switch', 'router'];
  return tiposValidos.includes(tipo.toLowerCase());
}


function agregarDispositivo(dispositivo) {

  if (!esIPValida(dispositivo.ip)) {
    console.log(`Error: La dirección IP ${dispositivo.ip} no es válida.`);
    return { exito: false, mensaje: `Error: La dirección IP ${dispositivo.ip} no es válida.` };
  }

  if (!esTipoDispositivoValido(dispositivo.tipo_dispositivo)) {
    console.log(`Error: Tipo de dispositivo ${dispositivo.tipo_dispositivo} no permitido.`);
    return { exito: false, mensaje: `Error: Tipo de dispositivo no permitido. Solo se aceptan 'switch' o 'router'.` };
  }
  
  const archivoDispositivos = path.join(__dirname, '..','..','topologia', 'inventarios', 'dispositivos.yaml');

  if (!fs.existsSync(archivoDispositivos)) {
    fs.writeFileSync(archivoDispositivos, yaml.dump({}), 'utf8');
  }

  try {
    let estructuraYaml = yaml.load(fs.readFileSync(archivoDispositivos, 'utf8')) || {};
    let dispositivoExistente = null;

    // Buscar si existe algún dispositivo con la misma IP
    for (const grupo in estructuraYaml) {
      for (const host in estructuraYaml[grupo].hosts) {
        if (estructuraYaml[grupo].hosts[host].host === dispositivo.ip) {
          dispositivoExistente = estructuraYaml[grupo].hosts[host];
          break;
        }
      }
      if (dispositivoExistente) break;
    }

    if (dispositivoExistente) {
      // Si existe un dispositivo con la misma IP, verifica que tipo y modelo sean iguales
      if (dispositivoExistente.tipo === dispositivo.tipo_dispositivo &&
          dispositivoExistente.marca === dispositivo.marca) {
        // Actualiza los datos del dispositivo existente
        dispositivoExistente.user = dispositivo.user;
        dispositivoExistente.password = dispositivo.password;
        dispositivoExistente.comunidad = dispositivo.comunidad;
        dispositivoExistente.region = dispositivo.region;
        dispositivoExistente.device_type = dispositivo.device_type;
        
        // Guardar cambios en el archivo
        fs.writeFileSync(archivoDispositivos, yaml.dump(estructuraYaml), 'utf8');
        console.log(`Se actualizaron los datos del dispositivo ${dispositivo.ip} como (${dispositivo.tipo_dispositivo}) y marca (${dispositivo.marca}).`);
        return { exito: true, mensaje: `Datos del dispositivo actualizados con éxito.` };
      } else {
        console.log(`Error: La IP ${dispositivo.ip} ya está asignada a otro tipo o modelo.`);
        return { exito: false, mensaje: `Error: La IP ${dispositivo.ip} ya está asignada a otro tipo o modelo.` };
      }
    } else {
      // Si no existe, crea una nueva entrada para el dispositivo
      const grupo = `${dispositivo.tipo_dispositivo.toLowerCase()}s_${dispositivo.marca.toLowerCase()}`;

      // Inicializar el grupo si no existe
      if (!estructuraYaml[grupo]) {
        estructuraYaml[grupo] = { hosts: {}, vars: {
          user: dispositivo.user,
          password: dispositivo.password,
          comunidad_snmp: dispositivo.comunidad,
          region_mstp: dispositivo.region,
          marca: dispositivo.marca,
          device_type: dispositivo.device_type,
        }};
      }

      const nuevoIndice = Object.keys(estructuraYaml[grupo].hosts).length + 1;
      const nuevaClave = `${dispositivo.tipo_dispositivo.toLowerCase()}${nuevoIndice}`;
      
      estructuraYaml[grupo].hosts[nuevaClave] = {
        host: dispositivo.ip,
        
      };

      // Escribe el archivo YAML con la nueva estructura
      fs.writeFileSync(archivoDispositivos, yaml.dump(estructuraYaml), 'utf8');
      console.log(`Nuevo dispositivo agregado con la IP ${dispositivo.ip}.`);
      return { exito: true, mensaje: `Nuevo dispositivo agregado con la IP ${dispositivo.ip}.` };
      
    }
  } catch (error) {
    console.error('Error al actualizar el archivo dispositivos.yaml:', error);
  }
}

function configure_snmp(req, res) {
  if (req.session.loggedin ){
    res.render('epops/snmp', {name: req.session.name});
  }else{
    res.redirect('/');
  }
      
}

function datosSNMP (datos){

  console.log('Received datos:', datos);

  
  const ipsInvalidas = datos.ip.filter(ip => !esIPValida(ip));
  if (ipsInvalidas.length > 0) {
    return { exito: false, mensaje: `Error: Las siguientes direcciones IP no son válidas: ${ipsInvalidas.join(', ')}` };
  }
  
  const archivoDispositivos = path.join(__dirname, '..', '..', 'topologia', 'inventarios', 'datos_snmp.yaml');
  // Aquí, asegúrate de que el archivo YAML existe o créalo con una estructura básica
  if (!fs.existsSync(archivoDispositivos)) {
    fs.writeFileSync(archivoDispositivos, yaml.dump({ datos_snmp: { hosts: {} } }), 'utf8');
  }

  try {
    let estructuraYaml = yaml.load(fs.readFileSync(archivoDispositivos, 'utf8')) || { datos_snmp: { hosts: {} } };
    let index = Object.keys(estructuraYaml.datos_snmp.hosts).length;
    let contadorswitch =1;

    // Limpia la estructura actual de hosts
    estructuraYaml.datos_snmp.hosts = {};

    datos.ip.forEach((ip, i) => {
      index++;
      estructuraYaml.datos_snmp.hosts[`switch${contadorswitch}`] = { host: ip };
      contadorswitch++;
    });

    // Establece los datos de usuario, comunidad y contraseña fuera del bucle
    estructuraYaml.datos_snmp.vars = {
      marca: datos.marca,
      comunidad: datos.comunidad,
      permisos: datos.permisos,
      id_list: datos.id_list,
      device_type: datos.device_type,
      usuario: datos.user,
      contrasena: datos.password,
    };

    // Escribe el archivo YAML con la nueva estructura
    fs.writeFileSync(archivoDispositivos, yaml.dump(estructuraYaml), 'utf8');
    console.log(`Configurando dispositivos con IPs: ${datos.ip.join(', ')}.`);
    return { exito: true, mensaje: `Configurando dispositivos con IPs: ${datos.ip.join(', ')}.` };
    
  } catch (error) {
    console.error('Error al actualizar el archivo datos_snmp.yaml:', error);
  }
}


function datosSTPActive (datos){

  console.log('Received datos:', datos);

  
  const ipsInvalidas = datos.ip.filter(ip => !esIPValida(ip));
  if (ipsInvalidas.length > 0) {
    return { exito: false, mensaje: `Error: Las siguientes direcciones IP no son válidas: ${ipsInvalidas.join(', ')}` };
  }
  
  const archivoDispositivos = path.join(__dirname, '..', '..', 'topologia', 'inventarios', 'datos_stp.yaml');
  // Aquí, asegúrate de que el archivo YAML existe o créalo con una estructura básica
  if (!fs.existsSync(archivoDispositivos)) {
    fs.writeFileSync(archivoDispositivos, yaml.dump({ datos_stp: { hosts: {} } }), 'utf8');
  }

  try {
    let estructuraYaml = yaml.load(fs.readFileSync(archivoDispositivos, 'utf8')) || { datos_stp: { hosts: {} } };
    let index = Object.keys(estructuraYaml.datos_stp.hosts).length;
    let contadorswitch =1;

    // Limpia la estructura actual de hosts
    estructuraYaml.datos_stp.hosts = {};

    datos.ip.forEach((ip, i) => {
      index++;
      estructuraYaml.datos_stp.hosts[`switch${contadorswitch}`] = { host: ip };
      contadorswitch++;
    });

    // Establece los datos de usuario, comunidad y contraseña fuera del bucle
    estructuraYaml.datos_stp.vars = {
      marca: datos.marca,
      modo: datos.modoSTP,
      region: datos.regionMSTP,
      device_type: datos.device_type,
      usuario: datos.user,
      contrasena: datos.password,
    };

    // Escribe el archivo YAML con la nueva estructura
    fs.writeFileSync(archivoDispositivos, yaml.dump(estructuraYaml), 'utf8');
    console.log(`Configurando dispositivos con IPs: ${datos.ip.join(', ')}.`);
    return { exito: true, mensaje: `Configurando dispositivos con IPs: ${datos.ip.join(', ')}.` };
    
  } catch (error) {
    console.error('Error al actualizar el archivo datos_snmp.yaml:', error);
  }
}

function datosSTPPriority (datos){

  console.log('Received datos:', datos);

  
  const ipsInvalidas = datos.ip.filter(ip => !esIPValida(ip));
  if (ipsInvalidas.length > 0) {
    return { exito: false, mensaje: `Error: Las siguientes direcciones IP no son válidas: ${ipsInvalidas.join(', ')}` };
  }
  
  // Validación de la prioridad
  const prioridad = parseInt(datos.prioridad);
  if (isNaN(prioridad) || prioridad < 0 || prioridad > 61440) {
    return { exito: false, mensaje: "Error: La prioridad debe ser un número entre 0 y 61440." };
  }

  const archivoDispositivos = path.join(__dirname, '..', '..', 'topologia', 'inventarios', 'datos_stpPriority.yaml');
  // Aquí, asegúrate de que el archivo YAML existe o créalo con una estructura básica
  if (!fs.existsSync(archivoDispositivos)) {
    fs.writeFileSync(archivoDispositivos, yaml.dump({ datos_stp: { hosts: {} } }), 'utf8');
  }

  try {
    let estructuraYaml = yaml.load(fs.readFileSync(archivoDispositivos, 'utf8')) || { datos_stp: { hosts: {} } };
    let index = Object.keys(estructuraYaml.datos_stp.hosts).length;
    let contadorswitch =1;

    // Limpia la estructura actual de hosts
    estructuraYaml.datos_stp.hosts = {};

    datos.ip.forEach((ip, i) => {
      index++;
      estructuraYaml.datos_stp.hosts[`switch${contadorswitch}`] = { host: ip };
      contadorswitch++;
    });

    // Establece los datos de usuario, comunidad y contraseña fuera del bucle
    estructuraYaml.datos_stp.vars = {
      marca: datos.marca,
      prioridad: datos.prioridad,
      vlan: datos.vlan,
      modo: datos.modo,
      instance: datos.instance,
      device_type: datos.device_type,
      usuario: datos.user,
      contrasena: datos.password,
    };

    // Escribe el archivo YAML con la nueva estructura
    fs.writeFileSync(archivoDispositivos, yaml.dump(estructuraYaml), 'utf8');
    console.log(`Configurando dispositivos con IPs: ${datos.ip.join(', ')}.`);
    return { exito: true, mensaje: `Configurando dispositivos con IPs: ${datos.ip.join(', ')}.` };
    
  } catch (error) {
    console.error('Error al actualizar el archivo datos_snmp.yaml:', error);
  }
}

function datosVLAN (datos){

  console.log('Received datos:', datos);

  
  const ipsInvalidas = datos.ip.filter(ip => !esIPValida(ip));
  if (ipsInvalidas.length > 0) {
    return { exito: false, mensaje: `Error: Las siguientes direcciones IP no son válidas: ${ipsInvalidas.join(', ')}` };
  }
  
  // Validación de la ID VLAN
  const idVlan = parseInt(datos.idVlan);
  if (isNaN(idVlan) || idVlan < 1 || idVlan > 1005 || idVlan === 1 || (idVlan >= 1002 && idVlan <= 1005)) {
    return {
      exito: false, 
      mensaje: "Error: La ID de la VLAN debe estar entre 1 y 1005, pero no puede ser 1, ni estar entre 1002 y 1005."
    };
  }

  const archivoDispositivos = path.join(__dirname, '..', '..', 'topologia', 'inventarios', 'datos_vlan.yaml');
  // Aquí, asegúrate de que el archivo YAML existe o créalo con una estructura básica
  if (!fs.existsSync(archivoDispositivos)) {
    fs.writeFileSync(archivoDispositivos, yaml.dump({ datos_vlan: { hosts: {} } }), 'utf8');
  }

  try {
    let estructuraYaml = yaml.load(fs.readFileSync(archivoDispositivos, 'utf8')) || { datos_vlan: { hosts: {} } };
    let index = Object.keys(estructuraYaml.datos_vlan.hosts).length;
    let contadorswitch =1;

    // Limpia la estructura actual de hosts
    estructuraYaml.datos_vlan.hosts = {};

    datos.ip.forEach((ip, i) => {
      index++;
      estructuraYaml.datos_vlan.hosts[`switch${contadorswitch}`] = { host: ip };
      contadorswitch++;
    });

    // Establece los datos de usuario, comunidad y contraseña fuera del bucle
    estructuraYaml.datos_vlan.vars = {
      marca: datos.marca,
      id: datos.idVlan,
      name_vlan: datos.name_vlan,
      device_type: datos.device_type,
      usuario: datos.user,
      contrasena: datos.password,
    };

    // Escribe el archivo YAML con la nueva estructura
    fs.writeFileSync(archivoDispositivos, yaml.dump(estructuraYaml), 'utf8');
    console.log(`Configurando dispositivos con IPs: ${datos.ip.join(', ')}.`);
    return { exito: true, mensaje: `Configurando dispositivos con IPs: ${datos.ip.join(', ')}.` };
    
  } catch (error) {
    console.error('Error al actualizar el archivo datos_snmp.yaml:', error);
  }
}

function datosLogs (datos){

  console.log('Received datos:', datos);

  
  const ipsInvalidas = datos.ip.filter(ip => !esIPValida(ip));
  if (ipsInvalidas.length > 0) {
    return { exito: false, mensaje: `Error: Las siguientes direcciones IP no son válidas: ${ipsInvalidas.join(', ')}` };
  }
  

  const archivoDispositivos = path.join(__dirname, '..', '..', 'topologia', 'inventarios', 'datos_logs.yaml');
  // Aquí, asegúrate de que el archivo YAML existe o créalo con una estructura básica
  if (!fs.existsSync(archivoDispositivos)) {
    fs.writeFileSync(archivoDispositivos, yaml.dump({ datos_logs: { hosts: {} } }), 'utf8');
  }

  try {
    let estructuraYaml = yaml.load(fs.readFileSync(archivoDispositivos, 'utf8')) || { datos_logs: { hosts: {} } };
    let index = Object.keys(estructuraYaml.datos_logs.hosts).length;
    let contadorswitch =1;

    // Limpia la estructura actual de hosts
    estructuraYaml.datos_logs.hosts = {};

    datos.ip.forEach((ip, i) => {
      index++;
      estructuraYaml.datos_logs.hosts[`switch${contadorswitch}`] = { host: ip };
      contadorswitch++;
    });

    estructuraYaml.datos_logs.vars = {
      marca: datos.marca,
      servidorIP: datos.servidorIP,
      trap: datos.trap,
      device_type: datos.device_type,
      usuario: datos.user,
      contrasena: datos.password,
    };

    // Escribe el archivo YAML con la nueva estructura
    fs.writeFileSync(archivoDispositivos, yaml.dump(estructuraYaml), 'utf8');
    console.log(`Configurando dispositivos con IPs: ${datos.ip.join(', ')}.`);
    return { exito: true, mensaje: `Configurando dispositivos con IPs: ${datos.ip.join(', ')}.` };
    
  } catch (error) {
    console.error('Error al actualizar el archivo datos_snmp.yaml:', error);
  }
}


function datosAcessList(datos){

  console.log('Received datos:', datos);

  const ipsInvalidas = datos.ip.filter(ip => !esIPValida(ip));
  if (ipsInvalidas.length > 0) {
    return { exito: false, mensaje: `Error: Las siguientes direcciones IP no son válidas: ${ipsInvalidas.join(', ')}` };
  }
  

  const archivoDispositivos = path.join(__dirname, '..', '..', 'topologia', 'inventarios', 'datos_access_list.yaml');
  // Aquí, asegúrate de que el archivo YAML existe o créalo con una estructura básica
  if (!fs.existsSync(archivoDispositivos)) {
    fs.writeFileSync(archivoDispositivos, yaml.dump({ datos_access_list: { hosts: {} } }), 'utf8');
  }

  try {
    let estructuraYaml = yaml.load(fs.readFileSync(archivoDispositivos, 'utf8')) || { datos_access_list: { hosts: {} } };
    let index = Object.keys(estructuraYaml.datos_access_list.hosts).length;
    let contadorswitch =1;

    // Limpia la estructura actual de hosts
    estructuraYaml.datos_access_list.hosts = {};

    datos.ip.forEach((ip, i) => {
      index++;
      estructuraYaml.datos_access_list.hosts[`switch${contadorswitch}`] = { host: ip };
      contadorswitch++;
    });

    // Establece los datos de usuario, comunidad y contraseña fuera del bucle
    estructuraYaml.datos_access_list.vars = {
      marca: datos.marca,
      ip_red: datos.ip_red,
      mascara_wildcard: datos.mascara_wildcard,
      id_list: datos.id_list,
      n_rule: datos.n_rule,
      device_type: datos.device_type,
      usuario: datos.user,
      contrasena: datos.password,
    };

    // Escribe el archivo YAML con la nueva estructura
    fs.writeFileSync(archivoDispositivos, yaml.dump(estructuraYaml), 'utf8');
    console.log(`Configurando dispositivos con IPs: ${datos.ip.join(', ')}.`);
    return { exito: true, mensaje: `Configurando dispositivos con IPs: ${datos.ip.join(', ')}.` };
    
  } catch (error) {
    console.error('Error al actualizar el archivo datos_access_list.yaml:', error);
  }
}


function guardarDispositivo(req, res) {
  const tipoFormulario = req.body.tipoFormulario;

  console.log(tipoFormulario);

  if (tipoFormulario === 'configuracion') {
    const resultado = agregarDispositivo(req.body);
    if (resultado.exito) {
      res.status(200).send(resultado.mensaje);
    } else {
      res.status(200).send(resultado.mensaje); 
    }
    
  } else if (tipoFormulario === 'data_snmp') {

    const resultado = datosSNMP(req.body);
    console.log(resultado);

    try {
      // Asegúrate de que la ruta al script Python sea correcta
      const pathToPythonScript = '/home/paola/Documentos/loginapp/modulo_automatizacion/snmp_int.py';
      const resPython = execSync(`python3 ${pathToPythonScript}`);
      console.log('Respuesta de Python:', resPython.toString());

      if (resultado.exito) {
        //res.status(200).send(resultado.mensaje);
        res.status(200).send(resPython.toString());
      } else {
        res.status(200).send(resultado.mensaje);
      }
    } catch (error) {
      console.error('Error ejecutando el script Python:', error);
      res.status(500).send('Error al procesar la configuración SNMP.');
    }
    
  } else if (tipoFormulario === 'stpActive') {

    const resultado = datosSTPActive(req.body);
    console.log(resultado);

    try {
      // Asegúrate de que la ruta al script Python sea correcta
      const pathToPythonScript = '/home/paola/Documentos/loginapp/modulo_automatizacion/stp_active_int.py';
      const resPython = execSync(`python3 ${pathToPythonScript}`);
      console.log('Respuesta de Python:', resPython.toString());

      if (resultado.exito) {
        res.status(200).send(resPython.toString());
      } else {
        res.status(200).send(resultado.mensaje);
      }
    } catch (error) {
      console.error('Error ejecutando el script Python:', error);
      res.status(500).send('Error al procesar la configuración STP.');
    }

  } else if (tipoFormulario === 'stpPriority') {

    const resultado = datosSTPPriority(req.body);
    console.log(resultado);

    try {
  
      const pathToPythonScript = '/home/paola/Documentos/loginapp/modulo_automatizacion/stp_priority_int.py';
      const resPython = execSync(`python3 ${pathToPythonScript}`);
      console.log('Respuesta de Python:', resPython.toString());

      if (resultado.exito) {
        res.status(200).send(resPython.toString());
      } else {
        res.status(200).send(resultado.mensaje);
      }
    } catch (error) {
      console.error('Error ejecutando el script Python:', error);
      res.status(500).send('Error al procesar la configuración STP.');
    }

  } else if (tipoFormulario === 'vlan') {

    const resultado = datosVLAN(req.body);
    console.log(resultado);

    try {
  
      const pathToPythonScript = '/home/paola/Documentos/loginapp/modulo_automatizacion/vlan_int.py';
      const resPython = execSync(`python3 ${pathToPythonScript}`);
      console.log('Respuesta de Python:', resPython.toString());

      if (resultado.exito) {
        res.status(200).send(resPython.toString());
      } else {
        res.status(200).send(resultado.mensaje);
      }
    } catch (error) {
      console.error('Error ejecutando el script Python:', error);
      res.status(500).send('Error al procesar la configuración de VLAN.');
    }

  } else if (tipoFormulario === 'logs') {

    const resultado = datosLogs(req.body);
    console.log(resultado);

    try {
  
      const pathToPythonScript = '/home/paola/Documentos/loginapp/modulo_automatizacion/logs_int.py';
      const resPython = execSync(`python3 ${pathToPythonScript}`);
      console.log('Respuesta de Python:', resPython.toString());

      if (resultado.exito) {
        res.status(200).send(resPython.toString());
      } else {
        res.status(200).send(resultado.mensaje);
      }
    } catch (error) {
      console.error('Error ejecutando el script Python:', error);
      res.status(500).send('Error al procesar la configuración de LOGS.');
    }  

  } else if (tipoFormulario === 'access_list') {

    const resultado = datosAcessList(req.body);

    try {
  
      const pathToPythonScript = '/home/paola/Documentos/loginapp/modulo_automatizacion/accesslist_int.py';
      const resPython = execSync(`python3 ${pathToPythonScript}`);
      console.log('Respuesta de Python:', resPython.toString());

      if (resultado.exito) {
        res.status(200).send(resPython.toString());
      } else {
        res.status(200).send(resultado.mensaje);
      }
    } catch (error) {
      console.error('Error ejecutando el script Python:', error);
      res.status(500).send('Error al procesar la configuración de LOGS.');
    }  

  } else {
      return res.status(400).send('Tipo de formulario inválido');
  } 
}


// Exportando todas las funciones
module.exports = {
    configure_archivo,
    configure_ini,
    guardarDispositivo,
    uploadYAMLFile,
    uploadYAML: uploadYAML.single('file'),  // Esto configura y exporta la función middleware
};