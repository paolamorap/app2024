/* ------------------------------------------------------------------------------------ */
/*-------------------------------++++ CLIENTE ++++--------------------------------------*/
/* ------------------------------------------------------------------------------------ */

if (document.getElementById('device-form')) {
  document.getElementById('device-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Previene la recarga de la página

    // Asignar el device_type basado en la selección de la marca
    const marcaSeleccionada = document.getElementById('marca').value;
    let device_type;
    if (marcaSeleccionada === 'CISCO') {
      device_type = 'cisco_ios';
    } else if (marcaSeleccionada === 'HP-A5120') {
        device_type = 'hp_comware';
    } 
    else {
        device_type = 'none';  
    }

    // Crea un objeto con los datos del formulario
    const formData = {
      tipo_dispositivo: document.getElementById('tipo_dispositivo').value,
      ip: document.getElementById('ip').value,
      marca: document.getElementById('marca').value,
      comunidad: document.getElementById('comunidad').value,
      region: document.getElementById('region').value,
      user: document.getElementById('user').value,
      password: document.getElementById('password').value,
      device_type: device_type,
      tipoFormulario: 'configuracion',
    };

    enviarFormData1(formData, '/configure','device-form');
  });
} else if(document.getElementById('snmp-form')){
    
  document.getElementById('snmp-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Previene la recarga de la página

    var idListInput = document.getElementById('id_list');
    var idListValue = idListInput.value.trim() === '' ? 'SN' : idListInput.value.trim();

    // Asignar el device_type basado en la selección de la marca
    const marcaSeleccionada = document.getElementById('marca').value;
    const permisosSNMP= document.getElementById('permisos').value;

    // Mapeos para device_type y permisos
    const deviceTypeMap = {
      'CISCO': 'cisco_ios',
      'HPA5120': 'hp_comware',
      // Añade más mapeos según sea necesario
    };

    const permissionsMap = {
      'CISCO': {
          'read': 'RO',
          'write': 'RW'
      },
      'HPA5120': {
          'read': 'read',
          'write': 'write'
      },
      'HPV1910': {
          'read': 'read',
          'write': 'write'
      },
      '3COM': {
          'read': 'read',
          'write': 'write'
      },
      'TPLINK': {
          'read': 'read-only',
          'write': 'read-write'
      }
    };

    // Determinar el tipo de dispositivo
    let device_type = deviceTypeMap[marcaSeleccionada] || 'none';

    // Determinar permisos
    let permisos = 'none';  // Valor por defecto para los permisos

    if (permissionsMap[marcaSeleccionada]) {
      permisos = permissionsMap[marcaSeleccionada][permisosSNMP] || 'none';
    }

    const formData = {
      ip: document.getElementById('ip').value.split(',').map(ip => ip.trim()),
      marca: document.getElementById('marca').value,
      comunidad: document.getElementById('comunidad').value,
      permisos: permisos,
      id_list: idListValue,
      user: document.getElementById('user').value,
      password: document.getElementById('password').value,
      device_type: device_type,
      tipoFormulario: 'data_snmp',
    };
    

    enviarFormData1(formData, '/snmp','snmp-form');
  });

} else if(document.getElementById('stpActive-form')){

  document.getElementById('stpActive-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Previene la recarga de la página

    // Asignar el device_type basado en la selección de la marca
    const marcaSeleccionada = document.getElementById('marca').value;
    let device_type;

    const modoSeleccionado = document.getElementById('modoSTP').value;
    let modo_stp;

    if (marcaSeleccionada === 'CISCO') {
      device_type = 'cisco_ios';
      if (modoSeleccionado == 'stp'){
        modo_stp = 'pvst';
      }else if(modoSeleccionado == 'rstp'){
        modo_stp = 'rapid-pvst';
      }else if (modoSeleccionado == 'mstp'){
        modo_stp = 'mst'
      }
    } else if (marcaSeleccionada === 'HPA5120') {
        device_type = 'hp_comware';
    } 
    else {
        device_type = 'none';  
        modo_stp = modoSeleccionado;
    }


    const formData = {
      ip: document.getElementById('ip').value.split(',').map(ip => ip.trim()),
      marca: document.getElementById('marca').value,
      modoSTP: modo_stp,
      regionMSTP: document.getElementById('modoSTP').value === 'mstp' ? document.getElementById('regionMSTP').value : 'region0',
      user: document.getElementById('user').value,
      password: document.getElementById('password').value,
      device_type: device_type,
      tipoFormulario: 'stpActive',
    };

    enviarFormData1(formData, '/stp','stpActive-form');
  });

} else if(document.getElementById('stpPriority-form')){
    
  document.getElementById('stpPriority-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Previene la recarga de la página

    // Asignar el device_type basado en la selección de la marca
    const marcaSeleccionada = document.getElementById('marca').value;
    let device_type;
    
    const modoSeleccionado = document.getElementById('modoSTP').value;
    let modo_stp;

    if (marcaSeleccionada === 'CISCO') {
      device_type = 'cisco_ios';
      if (modoSeleccionado == 'pvst'){
        modo_stp = 'pvst';
      }else if(modoSeleccionado == 'rpvst'){
        modo_stp = 'rapid-pvst';
      }else if (modoSeleccionado == 'mstp'){
        modo_stp = 'mst'
      }
    } else if (marcaSeleccionada === 'HPA5120') {
        device_type = 'hp_comware';
        modo_stp = modoSeleccionado;
    } 
    else {
        device_type = 'none';  
        modo_stp = modoSeleccionado;
    }

    const formData = {
      ip: document.getElementById('ip').value.split(',').map(ip => ip.trim()),
      marca: document.getElementById('marca').value,
      modo: modo_stp,
      vlan: document.getElementById('marca').value === 'TPLINK' || document.getElementById('modoSTP').value === 'pvst' || document.getElementById('modoSTP').value === 'rpvst' ? document.getElementById('vlan').value : 'none',
      instance: document.getElementById('modoSTP').value === 'mstp' ? document.getElementById('instance').value : 'none', // Added this line
      prioridad: document.getElementById('prioridad').value,
      user: document.getElementById('user').value,
      password: document.getElementById('password').value,
      device_type: device_type,
      tipoFormulario: 'stpPriority',
    };

    enviarFormData1(formData, '/stp1','stpPriority-form');
  });

} else if(document.getElementById('vlan-form')){
    
  document.getElementById('vlan-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Previene la recarga de la página

    // Asignar el device_type basado en la selección de la marca

    const marcaSeleccionada = document.getElementById('marca').value;
    let device_type;
    if (marcaSeleccionada === 'CISCO') {
      device_type = 'cisco_ios';
    } else if (marcaSeleccionada === 'HPA5120') {
        device_type = 'hp_comware';
    } 
    else {
        device_type = 'none';  
    }
    
    const formData = {
      ip: document.getElementById('ip').value.split(',').map(ip => ip.trim()),
      marca: document.getElementById('marca').value,
      idVlan: document.getElementById('id_vlan').value,
      name_vlan: document.getElementById('name_vlan').value,
      device_type: device_type,
      user: document.getElementById('user').value,
      password: document.getElementById('password').value,
      tipoFormulario: 'vlan',
    };
    

    enviarFormData1(formData, '/vlan','vlan-form');
  });
} else if(document.getElementById('logs-form')){
    
  document.getElementById('logs-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Previene la recarga de la página

    // Asignar el device_type basado en la selección de la marca

    const marcaSeleccionada = document.getElementById('marca').value;
    let device_type;
    if (marcaSeleccionada === 'CISCO') {
      device_type = 'cisco_ios';
    } else if (marcaSeleccionada === 'HPA5120') {
        device_type = 'hp_comware';
    } 
    else {
        device_type = 'none';  
    }
    
    const formData = {
      ip: document.getElementById('ip').value.split(',').map(ip => ip.trim()),
      marca: document.getElementById('marca').value,
      servidorIP: document.getElementById('servidorIP').value,
      trap: document.getElementById('marca').value === 'CISCO' || document.getElementById('marca').value === 'TPLINK' ? document.getElementById('trap').value : 'none',
      device_type: device_type,
      user: document.getElementById('user').value,
      password: document.getElementById('password').value,
      tipoFormulario: 'logs',

    };
    
    enviarFormData1(formData, '/logs', 'logs-form');
  });
} else if(document.getElementById('uploadForm')){
    
  document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Previene la recarga de la página
    
    var formData = new FormData(this);
    enviarFormData1(formData, '/upload','uploadForm');
  });
} else if(document.getElementById('accesslist-form')){
    
  document.getElementById('accesslist-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Previene la recarga de la página

    // Asignar el device_type basado en la selección de la marca

    const marcaSeleccionada = document.getElementById('marca').value;
    let device_type;
    if (marcaSeleccionada === 'CISCO') {
      device_type = 'cisco_ios';
    } else if (marcaSeleccionada === 'HPA5120') {
        device_type = 'hp_comware';
    } 
    else {
        device_type = 'none';  
    }
    
    const formData = {
      ip: document.getElementById('ip').value.split(',').map(ip => ip.trim()),
      marca: document.getElementById('marca').value,
      ip_red: document.getElementById('ip_red').value,
      mascara_wildcard: document.getElementById('mascara_wildcard').value,
      id_list: document.getElementById('id_list').value,
      n_rule: document.getElementById('marca').value === 'HPA5120' || document.getElementById('marca').value === 'HPV1910' || document.getElementById('marca').value === '3COM' || document.getElementById('marca').value === 'TPLINK' ? document.getElementById('n_regla').value : 'none',
      device_type: device_type,
      user: document.getElementById('user').value,
      password: document.getElementById('password').value,
      tipoFormulario: 'access_list',

    };
    
    enviarFormData1(formData, '/access_list', 'accesslist-form');
  });
} else if(document.getElementById('stpCost-form')){
    
  document.getElementById('stpCost-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Previene la recarga de la página

    // Asignar el device_type basado en la selección de la marca
    const marcaSeleccionada = document.getElementById('marca').value;
    let device_type;

    const modoSeleccionado = document.getElementById('modoSTP').value;
    let modo_stp;
  
    if (marcaSeleccionada === 'CISCO') {
      device_type = 'cisco_ios';
      modo_stp = 'modo0';
    } else if (marcaSeleccionada === 'HPA5120') {
        device_type = 'hp_comware';
        modo_stp = modoSeleccionado;
    } 
    else {
        device_type = 'none';  
        modo_stp = modoSeleccionado;
    }

    const formData = {
      ip: document.getElementById('ip').value.split(',').map(ip => ip.trim()),
      interfaz: document.getElementById('interfaz').value,
      marca: document.getElementById('marca').value,
      modo: modo_stp,
      costo: document.getElementById('costo').value,
      vlan: document.getElementById('modoSTP').value === 'pvst' || document.getElementById('modoSTP').value === 'rpvst' ? document.getElementById('vlan').value : 'none',
      instance: document.getElementById('modoSTP').value === 'mstp' ? document.getElementById('instance').value : 'none', 
      user: document.getElementById('user').value,
      password: document.getElementById('password').value,
      device_type: device_type,
      tipoFormulario: 'stpCost',
    };

    enviarFormData1(formData, '/pathcost', 'stpCost-form');
  });
}

/* ------------------------------------------------------------------------------------ */
/*---------------++++ FUNCIONES PARA RECIBIR DATOS DE BLOQUES NUEVOS ++++---------------*/
/* ------------------------------------------------------------------------------------ */

function mostrarCampoLogs(marcaSeleccionada) {
  var campoCisco = document.getElementById('campoCisco');

  if (['CISCO','TPLINK'].includes(marcaSeleccionada)) {
    campoCisco.style.display = 'block';
  } 
  else {
    campoCisco.style.display = 'none';
  }
}

function mostrarCampoRegion(modoSeleccionado) {
  var campoRegionMSTP = document.getElementById('campoRegionMSTP');
  if(modoSeleccionado === 'mstp') {
    campoRegionMSTP.style.display = 'block';
  } else {
    campoRegionMSTP.style.display = 'none';
  }
}



function enviarFormData1(formData, url, formId) {
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(formData)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('La petición al servidor falló.');
    }
    return response.text();
  })
  .then(mensaje => {
    mostrarMensaje(mensaje, 'success');

    // Resetear el formulario tras una respuesta exitosa
    if (formId) {
      document.getElementById(formId).reset();
    }
  })
  .catch(error => {
    mostrarMensaje('Error: ' + error.message, 'error');
  });
}


function mostrarMensaje(mensaje, tipo) {
  var messageContainer = document.getElementById('message-container');
  messageContainer.textContent = mensaje;
  messageContainer.className = 'message-container ' + tipo;
  messageContainer.style.display = 'block';

  setTimeout(() => {
      messageContainer.style.display = 'none';
  }, 6000);
}


