document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("balanceo-form");

  form.addEventListener("submit", function(event) {
      event.preventDefault(); // Previene el envío del formulario por defecto

      // Extraer los valores de los campos del formulario
      const enlace = document.getElementById("enlace").value;
      const modoSTP = document.getElementById("modoSTP").value;
      const vlan1 = document.getElementById("vlan1").value;
      const user = document.getElementById("user").value;
      const password = document.getElementById("password").value;

      // Crear un objeto con los datos del formulario
      const formData = {
          enlace: enlace,
          modoSTP: modoSTP,
          vlan1: vlan1,
          user: user,
          password: password,
          tipoFormulario: 'balanceo',
      };

      // Opcional: enviar los datos al servidor usando fetch o AJAX
      fetch("/balanceo/procesar", {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
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
        if ('balanceo-form') {
          document.getElementById('balanceo-form').reset();
        }
      })
      .catch(error => {
        mostrarMensaje('Error: ' + error.message, 'error');
      });
       
  });

  function mostrarMensaje(mensaje, tipo) {
    var messageContainer = document.getElementById('message-container');
    messageContainer.textContent = mensaje;
    messageContainer.className = 'message-container ' + tipo;
    messageContainer.style.display = 'block';
  
    setTimeout(() => {
        messageContainer.style.display = 'none';
    }, 6000);
  }

});

