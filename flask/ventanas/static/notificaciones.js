function toggleNotificaciones() {
    // Obtener el contenedor de notificaciones
    var notificacionesContainer = document.getElementById('notificaciones-container');

    // Simular obtener las notificaciones de tu API (puedes hacer una solicitud AJAX aquí)
    var notificaciones = obtenerNotificaciones(); // Esta función debe devolver las notificaciones desde tu API

    // Limpiar el contenedor de notificaciones antes de agregar nuevas notificaciones
    notificacionesContainer.innerHTML = '';

    // Iterar sobre las notificaciones y agregarlas al contenedor
    notificaciones.forEach(function(notificacion) {
        var notificacionElement = document.createElement('div');
        notificacionElement.className = 'dropdown-item';
        notificacionElement.innerText = notificacion.texto; // Asegúrate de tener una propiedad 'texto' en tus objetos de notificación

        // Agregar la notificación al contenedor
        notificacionesContainer.appendChild(notificacionElement);
    });

    // Mostrar el contenedor de notificaciones
    notificacionesContainer.style.display = 'block';
}

// Función simulada para obtener las notificaciones desde tu API
function obtenerNotificaciones() {
    // Aquí deberías hacer una solicitud AJAX para obtener las notificaciones desde tu API
    // Por ahora, solo devolveré un array de ejemplo para fines de demostración
    return [
        { texto: 'Nueva notificación 1' },
        { texto: 'Nueva notificación 2' },
        // ... más notificaciones
    ];
}
