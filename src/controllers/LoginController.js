const bcrypt = require('bcrypt');

function login(req, res) {
  if (req.session.loggedin != true ){
    res.render('login/index');
  }else{
    res.redirect('/');
  }
    
  }

function auth(req, res) {
  const {login, password} = req.body;
  req.getConnection((err, conn) => {
    if (err) throw err;
    // Buscar tanto por email como por username
    conn.query('SELECT * FROM users WHERE email = ? OR username = ?', [login, login], (err, results) => {
      if (err) throw err;
      if (results.length > 0) {
        const user = results[0];
        bcrypt.compare(password, user.password, (err, isMatch) => {
          if (!isMatch) {
            res.render('login/index', { error: 'Error: Contraseña Incorrecta' });
          } else {
            // Configura la sesión con los datos del usuario
            req.session.loggedin = true;
            req.session.name = user.name;
            req.session.email = user.email;
            req.session.privilege = user.privilege;

            if (user.is_default_password) {
              res.render('login/updateAdmin');  // Página de actualización para admin
            } else {
              res.redirect('/');
            }
          }
        });
      } else {
        res.render('login/index', { error: 'Error: El Usuario no existe' });
      }
    });
  });
}


function updateAdmin(req, res) {
  const { email, password, name, username} = req.body;
  if (!req.session.loggedin || req.session.privilege !== 'admin') {
    return res.redirect('/login');  // Redirige a los no administradores
  }

  bcrypt.hash(password, 12, (err, hash) => {
    if (err) {
      res.render('login/updateAdmin', { error: 'Error al encriptar la contraseña' });
    } else {
      req.getConnection((err, conn) => {
        if (err) {
          return res.render('login/updateAdmin', { error: 'Error de conexión a la base de datos' });
        }
        conn.query('UPDATE users SET email = ?, password = ?, name = ?, username =?, is_default_password = FALSE WHERE email = ?', [email, hash, name, username, req.session.email], (err, results) => {
          if (err) {
            return res.render('login/updateAdmin', { error: 'Error al actualizar los datos' });
          }
          req.session.loggedin = true;
          req.session.email = email;  // Actualizar el email en la sesión
          req.session.name = name;    // Actualizar el nombre en la sesión
          req.session.username = username;
          res.redirect('/');  // Redirige al home
        });
      });
    }
  });
}

function updatePassword(req, res) {
  const { currentPassword, newPassword, confirmNewPassword } = req.body;

  if (!req.session.loggedin) {
    return res.redirect('/');
  }

  req.getConnection((err, conn) => {
    if (err) {
      res.render('error', { error: 'Error de conexión a la base de datos' });
      return;
    }

    conn.query('SELECT password FROM users WHERE email = ?', [req.session.email], (err, results) => {
      if (err || results.length === 0) {
        res.render('login/profile', { error: 'Usuario no encontrado', name: req.session.name, email: req.session.email });
        return;
      }

      const user = results[0];

      bcrypt.compare(currentPassword, user.password, (err, isMatch) => {
        if (!isMatch) {
          res.render('login/profile', { error: 'Contraseña actual incorrecta', name: req.session.name, email: req.session.email });
          return;
        }

        if (newPassword !== confirmNewPassword) {
          res.render('login/profile', { error: 'Las nuevas contraseñas no coinciden', name: req.session.name, email: req.session.email });
          return;
        }

        bcrypt.hash(newPassword, 12, (err, hash) => {
          if (err) {
            res.render('login/profile', { error: 'Error al encriptar la nueva contraseña', name: req.session.name, email: req.session.email });
            return;
          }

          conn.query('UPDATE users SET password = ?, is_default_password = FALSE WHERE email = ?', [hash, req.session.email], (err, results) => {
            if (err) {
              res.render('login/profile', { error: 'Error al actualizar la contraseña', name: req.session.name, email: req.session.email });
              return;
            }

            res.render('login/profile', { message: 'Contraseña actualizada correctamente', name: req.session.name, email: req.session.email });
          });
        });
      });
    });
  });
}


function showUpdateAdmin(req, res) {
  if (req.session.loggedin && req.session.privilege === 'admin') {
    // Solo permitir acceso a esta página si el usuario es un administrador logueado
    res.render('login/updateAdmin');  // Asegúrate de que la ruta del archivo sea correcta
  } else {
    // Si no es administrador o no está logueado, redirige al login
    res.redirect('/');
  }
}

function showProfile(req, res) {
  if (!req.session.loggedin) {
    return res.redirect('/');  // Redirigir si no está logueado
  }
  res.render('login/profile', {
    name: req.session.name,
    email: req.session.email
  });
}

  
function register(req, res) {
  if (req.session.loggedin == true) {
    res.render('login/register', { name: req.session.name }); // Asegúrate de pasar la información del usuario.
  } else {
    res.redirect('/');
  }
}


  function printuser(req, res) {
    const { name, email, username, password, role } = req.body;
  
    req.getConnection((err, conn) => {
      if (err) {
        res.render('login/register', { error: 'Error de conexión a la base de datos' });
        return;
      }
  
      conn.query('SELECT * FROM users WHERE email = ? OR username = ?', [email, username], (err, results) => {
        if (err) {
          res.render('login/register', { error: 'Error al verificar el usuario' });
          return;
        }
  
        if (results.length > 0) {
          res.render('login/register', { error: 'Error: Usuario ya creado' });
        } else {
          bcrypt.hash(password, 12, (err, hash) => {
            if (err) {
              res.render('login/register', { error: 'Error al encriptar la contraseña' });
              return;
            }
  
            const newUser = {
              name: name,
              username: username,
              email: email,
              password: hash,
              is_default_password: false,
              privilege: role
            };
  
            conn.query('INSERT INTO users SET ?', newUser, (err, result) => {
              if (err) {
                res.render('login/register', { error: 'Error al registrar el usuario' });
                return;
              }
  
              // Configura la sesión si es necesario, o simplemente redirige
              req.session.loggedin = true;
              req.session.name = name;
              res.redirect('/');
            });
          });
        }
      });
    });
  }
  

  function logout (req, res) {
    if (req.session.loggedin ==true){
      req.session.destroy();
      res.redirect('/')
    }else{
      res.redirect('/')
    }
  }

  
  
  module.exports = {
    login: login,
    register: register,
    printuser: printuser,
    auth: auth,
    logout: logout,
    updateAdmin: updateAdmin,
    showUpdateAdmin: showUpdateAdmin,
    showProfile: showProfile,
    updatePassword: updatePassword,
  }