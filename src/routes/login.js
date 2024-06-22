const express = require('express');

const LoginController = require('../controllers/LoginController');
const AutoController = require('../controllers/AutoController');
const TopoController = require('../controllers/TopoController');
const OperaController = require('../controllers/OperaController')

const router = express.Router();

// Aquí incorporas las rutas para la carga de archivos YAML

router.get('/login', LoginController.login);
router.post('/login', LoginController.auth);
router.get('/update-admin', LoginController.showUpdateAdmin);  // Muestra la página de actualización para admin
router.post('/update-admin', LoginController.updateAdmin);
router.get('/register', LoginController.register);
router.post('/register', LoginController.printuser);
router.get('/logout', LoginController.logout);

//RUTAS PARA PERIFIL DE USUARIO Y ACTUALIZAR CONTRASENA
router.get('/profile', LoginController.showProfile);
router.post('/updatePassword', LoginController.updatePassword);

//RUTAS PARA CONFIGURAR ARCHIVO YAML
router.get('/configure', AutoController.configure_ini);
router.post('/configure', AutoController.guardarDispositivo);
router.get('/upload', AutoController.configure_archivo);
router.post('/upload', AutoController.uploadYAML, AutoController.uploadYAMLFile);



//RUTA PARA VISUALIZAR TOPOLOGIA
//router.get('/topologia', TopoController.topo_ini);
router.get('/topologia', TopoController.chageDetect);
router.post('/topologia', TopoController.update_Topology)
router.get('/check-change', TopoController.checkChange);

//RUTA PARA VISUALIZAR OPERACIONES
router.get('/operaciones', TopoController.operaciones_ini);
router.get('/configuracion-aplicacion', TopoController.configuraciones_ini);
router.get('/run1', OperaController.cargarArchivo);

router.get('/balanceo', OperaController.balanceo);
router.post('/balanceo/procesar', OperaController.ejecutarBalanceo);

//RUTAS DENTRO DEL MODULO DE OPERACIONES
router.get('/snmp', OperaController.snmp);
router.post('/snmp', AutoController.guardarDispositivo);

router.get('/access_list', OperaController.access_list);
router.post('/access_list', AutoController.guardarDispositivo);

router.get('/stp', OperaController.stp);
router.post('/stp', AutoController.guardarDispositivo);

router.get('/stp1', OperaController.stp1);
router.post('/stp1', AutoController.guardarDispositivo);

router.get('/pathcost', OperaController.pathcost);
router.post('/pathcost', AutoController.guardarDispositivo);

router.get('/vlan', OperaController.vlan);
router.post('/vlan', AutoController.guardarDispositivo);

router.get('/logs', OperaController.logs);
router.post('/logs', AutoController.guardarDispositivo);

//RUTA PARA INICAR LA APP

router.get('/start_app', OperaController.start_app);
router.get('/run_script', OperaController.run_script);  

router.get('/stop_app', OperaController.stop_app);
router.get('/stop_algoritmo', OperaController.stop);  

//BALANCEO DE CARGA
//router.post('/balanceo', OperaController.cargarArchivo);




module.exports = router;

