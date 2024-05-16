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

      // Mostrar los datos en la consola (para depuración)
      console.log("Datos del formulario:", formData);

      // Opcional: enviar los datos al servidor usando fetch o AJAX
      fetch("/balanceo", {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify(formData)
      })
      .then(response => response.json())
      .then(data => {
          // Manejar la respuesta del servidor
          console.log("Respuesta del servidor:", data);
          const messageContainer = document.getElementById("message-container");
          messageContainer.innerHTML = `<p>${data.message}</p>`;
      })
      .catch(error => {
          console.error("Error al enviar los datos:", error);
      });
  });
});
