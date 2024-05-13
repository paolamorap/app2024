const bcrypt = require('bcrypt');
const saltRounds = 10;
const myPassword = 'admin';  // Reemplaza 'tu_contraseña' con la contraseña que deseas hashear

bcrypt.hash(myPassword, saltRounds, function(err, hash) {
    if (err) {
        console.error(err);
        return;
    }
    console.log("Hash generado:", hash);
});
