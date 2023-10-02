function toggleNotificaciones() {
    var notificacionesContainer = document.getElementById('notificaciones-container');
    notificacionesContainer.innerHTML = '';

    // Realizar una solicitud AJAX para obtener las notificaciones desde la API
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/comentarios', true);
    xhr.onload = function() {
        if (xhr.status === 200) {
            var notificaciones = JSON.parse(xhr.responseText);

            notificaciones.forEach(function(notificacion) {
                var notificacionElement = document.createElement('a');
                notificacionElement.className = 'dropdown-item';
                notificacionElement.href = '/detalle_duda' + notificacion.duda_id; 
                notificacionElement.innerText = notificacion.nombre_usuario_comentario + ' ha respondido a tu duda de ' + notificacion.asignatura;
                notificacionesContainer.appendChild(notificacionElement);
            });

            notificacionesContainer.style.display = 'block';
        } else {
            console.error('Error al obtener las notificaciones: ' + xhr.status);
        }
    };
    xhr.onerror = function() {
        console.error('Error de red al obtener las notificaciones');
    };
    xhr.send();
}

// Evento de clic para los elementos de notificación
document.addEventListener("DOMContentLoaded", function() {
    toggleNotificaciones(); // Llama a la función cuando el documento está completamente cargado

    // Añade el evento de clic a los elementos de notificación
    var notificacionesContainer = document.getElementById('notificaciones-container');
    notificacionesContainer.addEventListener('click', function(event) {
        // Verifica si el elemento clicado es un enlace (<a>)
        if (event.target.tagName === 'A') {
            // Redirige a la URL del enlace
            window.location.href = event.target.href;
        }
    });
});