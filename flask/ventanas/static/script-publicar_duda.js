function limitarPalabras(elemento, maxPalabras) {
    var valor = elemento.value;
    var palabras = valor.trim().split(/\s+/);
    
    if (palabras.length > maxPalabras) {
      palabras = palabras.slice(0, maxPalabras);
      elemento.value = palabras.join(" ");
    }
}
  






function mostrarVistaPrevia(asignatura) {
    const fileInput = document.getElementById('imagen');
    const previewContainer = document.getElementById('vista-previa');
    const previewImage = document.createElement('img');

    // Eliminar la vista previa anterior si existe
    while (previewContainer.firstChild) {
        previewContainer.removeChild(previewContainer.firstChild);
    }

    // Verificar si se proporcionó una asignatura como argumento
    if (asignatura) {
        // Llamar a la función para actualizar curso y carrera con la asignatura proporcionada
        updateAsignaturas(asignatura);
    }

    // Verificar si se seleccionó un archivo
    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];

        // Verificar si el archivo es una imagen
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();

            reader.onload = function (e) {
                // Crear la etiqueta de imagen y establecer su atributo src con los datos de la imagen
                previewImage.src = e.target.result;
                previewContainer.appendChild(previewImage);

                // Convertir la imagen a bytes (base64)
                const imagenBase64 = e.target.result;
                const byteCharacters = atob(imagenBase64.split(',')[1]);
                const byteNumbers = new Array(byteCharacters.length);
                for (let i = 0; i < byteCharacters.length; i++) {
                    byteNumbers[i] = byteCharacters.charCodeAt(i);
                }
                const byteArray = new Uint8Array(byteNumbers);

                // Hacer una solicitud POST a la API para clasificar el texto
                fetch('/api/predecir_texto', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/octet-stream',
                    },
                    body: byteArray,
                })
                    .then(response => response.json())
                    .then(data => {
                        // Rellenar el campo de asignatura en el formulario con los resultados obtenidos
                        document.getElementById('asignatura').value = data.asignatura;

                        // Llamar a la función para actualizar curso y carrera
                        updateAsignaturas(data.asignatura);
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            };

            // Leer el contenido del archivo como URL
            reader.readAsDataURL(file);
        } else {
            // Mostrar un mensaje de error si el archivo no es una imagen
            const errorMessage = document.createElement('p');
            errorMessage.textContent = 'El archivo seleccionado no es una imagen válida.';
            previewContainer.appendChild(errorMessage);
        }
    } else {
        // Mostrar un mensaje de error si no se seleccionó ningún archivo
        const errorMessage = document.createElement('p');
        errorMessage.textContent = 'Por favor, selecciona una imagen.';
        previewContainer.appendChild(errorMessage);
    }
}







  
function borrarImagen() {
    const fileInput = document.getElementById('imagen');
    fileInput.value = ''; // Borra el valor del input de archivo
  
    const previewContainer = document.getElementById('vista-previa');
    while (previewContainer.firstChild) {
      previewContainer.removeChild(previewContainer.firstChild);
    }
}
  


var asignaturasDefinidas = {
        "Fundamentos de Organización de las TIC": { carrera: "ISI", curso: "1º" },
        "Fundamentos Físicos de la Informática I": { carrera: "ISI", curso: "1º" },
        "Fundamentos Matemáticos de la Informática I": { carrera: "ISI", curso: "1º" },
        "Fundamentos Matemáticos de la Informática II": { carrera: "ISI", curso: "1º" },
        "Introducción a la Ingeniería Informática": { carrera: "ISI", curso: "1º" },
        "Modelos de Computación": { carrera: "ISI", curso: "1º" },
        "Programación I": { carrera: "ISI", curso: "1º" },
        "Programación II": { carrera: "ISI", curso: "1º" },
        "Claves de Historia Contemporánea": { carrera: "ISI", curso: "1º" },
        // Agrega más asignaturas según sea necesario
        // ...

        // Agregar asignaturas para ADE
        "Politica": { carrera: "ADE", curso: "1º" },
        // Resto de las asignaturas para ADE...
        // ...
};
function updateAsignaturas(asignatura) {
    var carreraSelect = document.getElementById("carrera");
    var cursoSelect = document.getElementById("curso");
    var asignaturaSelect = document.getElementById("asignatura");

    // Limpia las opciones actuales del desplegable de asignaturas
    asignaturaSelect.innerHTML = "";

    // Toma la asignatura directamente del campo en el formulario si no se proporciona como argumento
    asignatura = asignatura || asignaturaSelect.value.trim();

    // Busca la información de carrera y curso basándose en la asignatura
    var infoAsignatura = asignaturasDefinidas[asignatura];

    if (infoAsignatura) {
        // Añade la asignatura al desplegable
        var option = document.createElement("option");
        option.text = asignatura;
        option.value = asignatura;
        asignaturaSelect.add(option);

        // Establece los valores de carrera y curso
        carreraSelect.value = infoAsignatura.carrera;
        cursoSelect.value = infoAsignatura.curso;
    } else {
        console.error("No se encontró información para la asignatura: " + asignatura);
    }
}


updateAsignaturas();


