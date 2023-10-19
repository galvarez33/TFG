document.getElementById('formulario').onsubmit = function(event) {
    event.preventDefault(); // Evitar que el formulario se envíe automáticamente
    
    // Obtener los datos del formulario
    var imagen = document.getElementById('imagen').files[0];
    var titulo = document.getElementById('titulo').value;
    var texto = document.getElementById('texto').value;
    // ... obtener otros datos del formulario
    
    // Crear un objeto FormData para enviar datos al servidor
    var formData = new FormData();
    formData.append('imagen', imagen);
    formData.append('titulo', titulo);
    formData.append('texto', texto);
    // ... agregar otros datos al formData si es necesario
    
    // Enviar los datos al servidor para su validación con TensorFlow
    fetch('/validar_duda', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.validacionExitosa) {
            // Si la validación es exitosa, enviar el formulario
            document.getElementById('formulario').submit();
        } else {
            // Mostrar un mensaje de error al usuario
            alert('Contenido no válido. Por favor, revise su duda antes de enviarla.');
        }
    });
};
