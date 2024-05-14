const multer = require('multer');
const yaml = require('js-yaml');
const path = require('path');
const fs = require('fs');
const {existsSync, execSync} = require('child_process')

/* ----------------------------------------------------------------------------------
********************** FUNCION PARA SUBIR EL ARCHIVO YAML ***************************
-----------------------------------------------------------------------------------*/

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
      const newName = "dispositivos1" + path.extname(file.originalname); 
      cb(null, newName);
  }
});

const uploadYAML = multer({ storage: storageYAML });

function uploadYAMLFile(req, res) {
  console.log(req.file);  // Log para ver la información del archivo cargado
  if (!req.file) {
    return res.status(400).send('No se subió ningún archivo.');
  }
  res.json({ message: 'Archivo YAML subido exitosamente!' });
}

/* ----------------------------------------------------------------------------------
********************** FUNCIONES PARA VISUALIZAR EN LA WEB **************************
-----------------------------------------------------------------------------------*/

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

/* ----------------------------------------------------------------------------------
*************************** FUNCIONES DE COMPROBACION *******************************
-----------------------------------------------------------------------------------*/
  
function esIPValida(ip) {
  const regexIP = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
  return regexIP.test(ip);
}

function esTipoDispositivoValido(tipo) {
  const tiposValidos = ['switch', 'router'];
  return tiposValidos.includes(tipo.toLowerCase());
}

/* -----------------------------------------------------------------------------------------
********************** FUNCIONES ALMACENAR DATOS EN ARCHIVOS YAML **************************
------------------------------------------------------------------------------------------*/

function agregarDispositivo(dispositivo) {
  /**
   * Agrega un dispositivo a un archivo YAML de inventario.
   *
   * @param {Object} dispositivo - Objeto que representa el dispositivo a agregar.
   * @param {string} dispositivo.ip - La dirección IP del dispositivo.
   * @param {string} dispositivo.tipo_dispositivo - El tipo de dispositivo ('switch' o 'router').
   * @param {string} dispositivo.marca - La marca del dispositivo.
   * @param {string} dispositivo.user - El usuario del dispositivo.
   * @param {string} dispositivo.password - La contraseña del dispositivo.
   * @param {string} dispositivo.comunidad - La comunidad SNMP del dispositivo.
   * @param {string} dispositivo.region - La región MSTP del dispositivo.
   * @param {string} dispositivo.device_type - El tipo de dispositivo específico.
   *
   * @returns {Object} - Objeto con las propiedades `exito` (booleano) y `mensaje` (string) indicando el resultado de la operación.
   */
  
  // Verifica si la dirección IP del dispositivo es válida
  if (!esIPValida(dispositivo.ip)) {
    console.log(`Error: La dirección IP ${dispositivo.ip} no es válida.`);
    return { exito: false, mensaje: `Error: La dirección IP ${dispositivo.ip} no es válida.` };
  }


  
  // Define la ruta del archivo YAML de dispositivos
  const archivoDispositivos = path.join(__dirname, '..','..','topologia', 'inventarios', 'dispositivos.yaml');

  // Si el archivo no existe, lo crea con una estructura vacía
  if (!fs.existsSync(archivoDispositivos)) {
    fs.writeFileSync(archivoDispositivos, yaml.dump({}), 'utf8');
  }

  console.log('Received datos:', dispositivo);

  try {
    // Carga el contenido del archivo YAML
    let estructuraYaml = yaml.load(fs.readFileSync(archivoDispositivos, 'utf8')) || {};
    let dispositivoExistente = null;

    // Busca si ya existe un dispositivo con la misma IP
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
      // Si el dispositivo existe, verifica que el tipo y la marca sean iguales
      if (dispositivoExistente.tipo === dispositivo.tipo_dispositivo &&
          dispositivoExistente.marca === dispositivo.marca) {
        // Actualiza los datos del dispositivo existente
        dispositivoExistente.user = dispositivo.user;
        dispositivoExistente.password = dispositivo.password;
        dispositivoExistente.comunidad = dispositivo.comunidad;
        dispositivoExistente.region = dispositivo.region;
        dispositivoExistente.device_type = dispositivo.device_type;
        
        // Guarda los cambios en el archivo
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
          tipo: dispositivo.tipo_dispositivo,
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
    return { exito: false, mensaje: 'Error al actualizar el archivo dispositivos.yaml.' };
  }
}
   
function datosSNMP(datos) {
  /**
   * Almacena datos SNMP para una lista de dispositivos y los guarda en un archivo YAML.
   *
   * @param {Object} datos - Objeto que contiene la información de los dispositivos.
   * @param {Array<string>} datos.ip - Lista de direcciones IP de los dispositivos.
   * @param {string} datos.marca - La marca de los dispositivos.
   * @param {string} datos.comunidad - La comunidad SNMP de los dispositivos.
   * @param {string} datos.permisos - El permiso de escritura o lectura de la comunidad SNMP.
   * @param {string} datos.id_list - Id del Access List permitido.
   * @param {string} datos.device_type - El tipo de dispositivo específico.
   * @param {string} datos.user - El usuario para acceder a los dispositivos.
   * @param {string} datos.password - La contraseña para acceder a los dispositivos.
   *
   * @returns {Object} - Objeto con las propiedades `exito` (booleano) y `mensaje` (string) indicando el resultado de la operación.
   */
  
  // Imprime los datos recibidos en la consola para propósitos de debugging
  console.log('Received datos:', datos);

  // Filtra las direcciones IP no válidas
  const ipsInvalidas = datos.ip.filter(ip => !esIPValida(ip));
  if (ipsInvalidas.length > 0) {
    return { exito: false, mensaje: `Error: Las siguientes direcciones IP no son válidas: ${ipsInvalidas.join(', ')}` };
  }

  // Define la ruta del archivo YAML de datos SNMP
  const archivoDispositivos = path.join(__dirname, '..', '..', 'modulo_automatizacion', 'registros', 'datos_snmp.yaml');

  // Si el archivo no existe, lo crea con una estructura básica
  if (!fs.existsSync(archivoDispositivos)) {
    fs.writeFileSync(archivoDispositivos, yaml.dump({ datos_snmp: { hosts: {} } }), 'utf8');
  }

  try {
    // Carga el contenido del archivo YAML
    let estructuraYaml = yaml.load(fs.readFileSync(archivoDispositivos, 'utf8')) || { datos_snmp: { hosts: {} } };
    let index = Object.keys(estructuraYaml.datos_snmp.hosts).length;
    let contadorswitch = 1;

    // Limpia la estructura actual de hosts
    estructuraYaml.datos_snmp.hosts = {};

    // Añade las IPs de los dispositivos a la estructura YAML
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
    return { exito: false, mensaje: 'Error al actualizar el archivo datos_snmp.yaml.' };
  }
}



function datosSTPActive (datos){

  console.log('Received datos:', datos);

  
  const ipsInvalidas = datos.ip.filter(ip => !esIPValida(ip));
  if (ipsInvalidas.length > 0) {
    return { exito: false, mensaje: `Error: Las siguientes direcciones IP no son válidas: ${ipsInvalidas.join(', ')}` };
  }
  
  const archivoDispositivos = path.join(__dirname, '..', '..', 'modulo_automatizacion', 'registros', 'datos_stp.yaml');
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
      vlan: datos.vlan,
      device_type: datos.device_type,
      usuario: datos.user,
      contrasena: datos.password,
    };

    // Escribe el archivo YAML con la nueva estructura
    fs.writeFileSync(archivoDispositivos, yaml.dump(estructuraYaml), 'utf8');
    console.log(`Configurando dispositivos con IPs: ${datos.ip.join(', ')}.`);
    return { exito: true, mensaje: `Configurando dispositivos con IPs: ${datos.ip.join(', ')}.` };
    
  } catch (error) {
    console.error('Error al actualizar el archivo datos_STPActive.yaml:', error);
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

  const archivoDispositivos = path.join(__dirname, '..', '..', 'modulo_automatizacion', 'registros', 'datos_stpPriority.yaml');
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
    console.error('Error al actualizar el archivo datos_STPPriority.yaml:', error);
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

  const archivoDispositivos = path.join(__dirname, '..', '..', 'modulo_automatizacion', 'registros', 'datos_vlan.yaml');
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
    console.error('Error al actualizar el archivo datos_vlan.yaml:', error);
  }
}

function datosLogs (datos){

  console.log('Received datos:', datos);

  
  const ipsInvalidas = datos.ip.filter(ip => !esIPValida(ip));
  if (ipsInvalidas.length > 0) {
    return { exito: false, mensaje: `Error: Las siguientes direcciones IP no son válidas: ${ipsInvalidas.join(', ')}` };
  }
  

  const archivoDispositivos = path.join(__dirname, '..', '..', 'modulo_automatizacion', 'registros', 'datos_logs.yaml');
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
    console.error('Error al actualizar el archivo datos_logs.yaml:', error);
  }
}


function datosAcessList(datos){

  console.log('Received datos:', datos);

  const ipsInvalidas = datos.ip.filter(ip => !esIPValida(ip));
  if (ipsInvalidas.length > 0) {
    return { exito: false, mensaje: `Error: Las siguientes direcciones IP no son válidas: ${ipsInvalidas.join(', ')}` };
  }
  

  const archivoDispositivos = path.join(__dirname, '..', '..', 'modulo_automatizacion', 'registros', 'datos_access_list.yaml');
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
      const pathToPythonScript = '/home/paola/Documentos/app2024/modulo_automatizacion/snmp_int.py';
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
      const pathToPythonScript = '/home/paola/Documentos/app2024/modulo_automatizacion/stp_active_int.py';
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
  
      const pathToPythonScript = '/home/paola/Documentos/app2024/modulo_automatizacion/stp_priority_int.py';
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
  
      const pathToPythonScript = '/home/paola/Documentos/app2024/modulo_automatizacion/vlan_int.py';
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
  
      const pathToPythonScript = '/home/paola/Documentos/app2024/modulo_automatizacion/logs_int.py';
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
  
      const pathToPythonScript = '/home/paola/Documentos/app2024/modulo_automatizacion/accesslist_int.py';
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