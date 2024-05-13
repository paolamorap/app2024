const express = require('express');
const { engine } = require('express-handlebars');
const myconnection = require('express-myconnection');
const mysql = require('mysql');
const session = require('express-session');
const bodyParser = require('body-parser');
const path = require('path');
var https = require('https'); 
var fs = require('fs');
const loginRoutes = require('./routes/login');
const multer = require('multer');

const app = express();

const PUERTO = 443;

const server = https.createServer({
    key: fs.readFileSync('/home/paola/Documentos/loginapp/http/localhost.key'),
    cert: fs.readFileSync('/home/paola/Documentos/loginapp/http/localhost.crt')
}, app).listen(PUERTO, function(){
    console.log('Escuchando en el puerto 443');
});

app.set('views', __dirname + '/views');
app.engine('.hbs', engine({
    extname: '.hbs'
}));
app.set('view engine', 'hbs');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.use(myconnection(mysql, {
    host: 'localhost',
    user: 'root',
    password: 'pollito0101',
    port: 3306,
    database: 'curso'
}));

app.use(session({
    secret: 'secret',
    resave: true,
    saveUninitialized: true
}));

app.use(express.static(path.join(__dirname, 'public')));
app.use(express.static(path.join(__dirname, 'configure')));
app.use(express.static(path.join(__dirname, 'next')));
app.use(express.static(path.join(__dirname, '..', '..', 'topologia', 'inventarios')));


app.use('/', loginRoutes);


app.get('/', (req, res) => {
    if (req.session.loggedin) {
        // Verificar el privilegio del usuario
        if (req.session.privilege === 'admin') {
            res.render('home', { name: req.session.name, isAdmin: req.session.privilege === 'admin' }); // Página para administradores
        } else {
            res.render('homeOperadores', { name: req.session.name }); // Página para usuarios no administradores
        }
    } else {
        res.redirect('/login'); // Redirigir a los usuarios no autenticados a la página de inicio de sesión
    }
});