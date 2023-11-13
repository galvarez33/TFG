function limitarPalabras(elemento, maxPalabras) {
    var valor = elemento.value;
    var palabras = valor.trim().split(/\s+/);
    
    if (palabras.length > maxPalabras) {
      palabras = palabras.slice(0, maxPalabras);
      elemento.value = palabras.join(" ");
    }
}
  






function mostrarVistaPrevia() {
    const fileInput = document.getElementById('imagen');
    const previewContainer = document.getElementById('vista-previa');
    const previewImage = document.createElement('img');

    // Eliminar la vista previa anterior si existe
    while (previewContainer.firstChild) {
        previewContainer.removeChild(previewContainer.firstChild);
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
                fetch('http://localhost:5001/api/predecir_texto', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/octet-stream',
                    },
                    body: byteArray,
                })

                .then(response => response.json())
                .then(data => {
                    // Rellenar el campo de asignatura en el formulario con los resultados obtenidos
                    document.getElementById('asignatura').textContent = data.asignatura;
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
  

function updateAsignaturas() {
    var carreraSelect = document.getElementById("carrera");
    var cursoSelect = document.getElementById("curso");
    var asignaturaSelect = document.getElementById("asignatura");
    var carreraValue = carreraSelect.value;
    var cursoValue = cursoSelect.value;

    // Limpia las opciones actuales del desplegable de asignaturas
    asignaturaSelect.innerHTML = "";

    // Añade las opciones correspondientes a la carrera y curso seleccionados
    if (carreraValue === "ISI") {
        if (cursoValue === "1º") {
            var option1 = document.createElement("option");
            option1.text = "Fundamentos de Organización de las TIC";
            option1.value = "Fundamentos de Organización de las TIC";
            asignaturaSelect.add(option1);

            var option2 = document.createElement("option");
            option2.text = "Fundamentos Físicos de la Informática II";
            option2.value = "Fundamentos Físicos de la Informática II";
            asignaturaSelect.add(option2);

            var option3 = document.createElement("option");
            option3.text = "Fundamentos Matemáticos de la Informática I";
            option3.value = "Fundamentos Matemáticos de la Informática I";
            asignaturaSelect.add(option3);

            var option4 = document.createElement("option");
            option4.text = "Fundamentos Matemáticos de la Informática II";
            option4.value = "Fundamentos Matemáticos de la Informática II";
            asignaturaSelect.add(option4);

            var option5 = document.createElement("option");
            option5.text = "Introducción a la Ingeniería Informática";
            option5.value = "Introducción a la Ingeniería Informática";
            asignaturaSelect.add(option5);

            var option6 = document.createElement("option");
            option6.text = "Modelos de Computación";
            option6.value = "Modelos de Computación";
            asignaturaSelect.add(option6);

            var option7 = document.createElement("option");
            option7.text = "Programación I";
            option7.value = "Programación I";
            asignaturaSelect.add(option7);

            var option8 = document.createElement("option");
            option8.text = "Programación II";
            option8.value = "Programación II";
            asignaturaSelect.add(option8);

            var option9 = document.createElement("option");
            option9.text = "Claves de Historia Contemporánea";
            option9.value = "Claves de Historia Contemporánea";
            asignaturaSelect.add(option9);
        } else if (cursoValue === "2º") {
            var option1 = document.createElement("option");
            option1.text = "Estadística";
            option1.value = "Estadística";
            asignaturaSelect.add(option1);

            var option2 = document.createElement("option");
            option2.text = "Análisis de los Estados Financieros";
            option2.value = "Análisis de los Estados Financieros";
            asignaturaSelect.add(option2);

            var option3 = document.createElement("option");
            option3.text = "Arquitectura de Ordenadores";
            option3.value = "Arquitectura de Ordenadores";
            asignaturaSelect.add(option3);

            var option4 = document.createElement("option");
            option4.text = "Bases de Datos I";
            option4.value = "Bases de Datos I";
            asignaturaSelect.add(option4);

            var option5 = document.createElement("option");
            option5.text = "Bases de Datos II";
            option5.value = "Bases de Datos II";
            asignaturaSelect.add(option5);

            var option6 = document.createElement("option");
            option6.text = "Gestión Financiera";
            option6.value = "Gestión Financiera";
            asignaturaSelect.add(option6);

            var option7 = document.createElement("option");
            option7.text = "Metodología y Tecnología de la Programación";
            option7.value = "Metodología y Tecnología de la Programación";
            asignaturaSelect.add(option7);

            var option8 = document.createElement("option");
            option8.text = "Redes de Ordenadores I";
            option8.value = "Redes de Ordenadores I";
            asignaturaSelect.add(option8);

            var option9 = document.createElement("option");
            option9.text = "Redes de Ordenadores II";
            option9.value = "Redes de Ordenadores II";
            asignaturaSelect.add(option9);

            var option10 = document.createElement("option");
            option10.text = "Sistemas Operativos";
            option10.value = "Sistemas Operativos";
            asignaturaSelect.add(option10);
        } else if (cursoValue === "3º") {
            var option1 = document.createElement("option");
            option1.text = "Administración de Sistemas de Información";
            option1.value = "Administración de Sistemas de Información";
            asignaturaSelect.add(option1);

            var option2 = document.createElement("option");
            option2.text = "Gestión Operativa de la Empresa TIC";
            option2.value = "Gestión Operativa de la Empresa TIC";
            asignaturaSelect.add(option2);

            var option3 = document.createElement("option");
            option3.text = "Infraestructuras de Sistemas de Información";
            option3.value = "Infraestructuras de Sistemas de Información";
            asignaturaSelect.add(option3);

            var option4 = document.createElement("option");
            option4.text = "Ingeniería del Software";
            option4.value = "Ingeniería del Software";
            asignaturaSelect.add(option4);

            var option5 = document.createElement("option");
            option5.text = "Inteligencia Artificial e Ingeniería del Conocimiento";
            option5.value = "Inteligencia Artificial e Ingeniería del Conocimiento";
            asignaturaSelect.add(option5);

            var option6 = document.createElement("option");
            option6.text = "Programación en Entornos Distribuidos";
            option6.value = "Programación en Entornos Distribuidos";
            asignaturaSelect.add(option6);

            var option7 = document.createElement("option");
            option7.text = "Proyectos de Sistemas de Información";
            option7.value = "Proyectos de Sistemas de Información";
            asignaturaSelect.add(option7);

            var option8 = document.createElement("option");
            option8.text = "Sistemas de Información en la Empresa I";
            option8.value = "Sistemas de Información en la Empresa I";
            asignaturaSelect.add(option8);

            var option9 = document.createElement("option");
            option9.text = "Sistemas de Información para la Dirección Estratégica";
            option9.value = "Sistemas de Información para la Dirección Estratégica";
            asignaturaSelect.add(option9);
        } else if (cursoValue === "4º") {
            var option1 = document.createElement("option");
            option1.text = "Doctrina Social de la Iglesia";
            option1.value = "Doctrina Social de la Iglesia";
            asignaturaSelect.add(option1);

            var option2 = document.createElement("option");
            option2.text = "Hombre y Mundo Moderno";
            option2.value = "Hombre y Mundo Moderno";
            asignaturaSelect.add(option2);

            var option3 = document.createElement("option");
            option3.text = "Recursos Humanos en las Empresas TIC";
            option3.value = "Recursos Humanos en las Empresas TIC";
            asignaturaSelect.add(option3);

            var option4 = document.createElement("option");
            option4.text = "Seguridad Informática y Protección de Datos";
            option4.value = "Seguridad Informática y Protección de Datos";
            asignaturaSelect.add(option4);

            var option5 = document.createElement("option");
            option5.text = "Sistemas Web I";
            option5.value = "Sistemas Web I";
            asignaturaSelect.add(option5);

            var option6 = document.createElement("option");
            option6.text = "Sistemas Web II";
            option6.value = "Sistemas Web II";
            asignaturaSelect.add(option6);

            var option7 = document.createElement("option");
            option7.text = "Trabajo de Fin de Grado";
            option7.value = "Trabajo de Fin de Grado";
            asignaturaSelect.add(option7);
        }
    } else if (carreraValue === "ADE") {
        if (cursoValue === "1º") {
            var option1 = document.createElement("option");
            option1.text = "Politica";
            option1.value = "Politica";
            asignaturaSelect.add(option1);

            // Resto de las opciones...
        } else if (cursoValue === "curso2") {
            // Agregar asignaturas para ADE - 2º
        } else if (cursoValue === "curso3") {
            // Agregar asignaturas para ADE - 3º
        } else if (cursoValue === "curso4") {
            // Agregar asignaturas para ADE - 4º
        } else if (cursoValue === "curso5") {
            // Agregar asignaturas para ADE - 5º
        }
    }

}



