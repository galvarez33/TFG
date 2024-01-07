"use strict";
import users from '../ranking.json' assert {type:'json'};
console.log(users)

// Definición de la función mostrarTabla
function mostrarTabla() {
    $('.table-container').toggle();
}

// Esta función se ejecutará cuando la página se cargue completamente
$(document).ready(function () {
    // Evento clic del botón
    $('#mostrarRankingBtn').click(function () {
        // Mostrar la ventana modal
        $('#tablaModal').modal('show');

        // Cargar y mostrar los datos del ranking.json
        cargarDatosRanking();
    });
});

function cargarDatosRanking() {
    // Utilizar XMLHttpRequest para obtener los datos del ranking.json
    var httpRequest = new XMLHttpRequest();
    httpRequest.open("GET", "../ranking.json", true);
    httpRequest.onreadystatechange = function () {
        if (this.readyState == 4) {
            if (this.status == 200) {
                var data = window.JSON ? JSON.parse(this.responseText) : eval("(" + this.responseText + ")");
                // Limpiar el cuerpo de la tabla antes de agregar nuevos datos
                $('#tabla-body').empty();
                
                // Iterar sobre los datos y agregar filas a la tabla
                $.each(data, function (correo, info) {
                    $('#tabla-body').append('<tr><td>' + info.nombre + '</td><td>' + info.puntos + '</td><td>' + info.posicion + '</td></tr>');
                });
            } else {
                console.error("HTTP error " + this.status + " " + this.statusText);
            }
        }
    };
    httpRequest.send();
    console.log("Solicitud enviada"); // Añadido para debug
}
