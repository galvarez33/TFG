document.addEventListener('DOMContentLoaded', function() {
    // Datos de ejemplo para las notificaciones
    var notificaciones = [
        { nombre: "Nombre1", asignatura: "Asignatura1", url: "/notificacion1" },
        { nombre: "Nombre2", asignatura: "Asignatura2", url: "/notificacion2" }
        // Agrega más notificaciones según sea necesario
    ];

    var notificacionesContainer = document.getElementById('notificaciones-container');

    function cargarNotificaciones() {
        var notificacionesHTML = '';

        // Generar HTML para las notificaciones con enlaces (href)
        notificaciones.forEach(function(notificacion) {
            notificacionesHTML += `<a class="dropdown-item" href="${notificacion.url}">${notificacion.nombre} ha respondido a tu duda de ${notificacion.asignatura}</a>`;
        });

        // Mostrar las notificaciones en el contenedor
        notificacionesContainer.innerHTML = notificacionesHTML;
    }

    function toggleNotificaciones(event) {
        // Prevenir el comportamiento predeterminado del enlace
        event.preventDefault();

        if (notificacionesContainer.style.display === 'block') {
            notificacionesContainer.style.display = 'none';
        } else {
            // Cargar y mostrar las notificaciones cuando se hace clic en el enlace
            cargarNotificaciones();
            notificacionesContainer.style.display = 'block';
        }
    }

    // Asociar la función toggleNotificaciones al clic del enlace
    var enlaceNotificaciones = document.querySelector('.nav-link');
    enlaceNotificaciones.onclick = toggleNotificaciones;
});
