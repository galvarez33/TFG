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
  
    // Borra la vista previa anterior si existe
    while (previewContainer.firstChild) {
      previewContainer.removeChild(previewContainer.firstChild);
    }
  
    const file = fileInput.files[0];
    if (file) {
      const reader = new FileReader();
      reader.addEventListener('load', function () {
        previewImage.setAttribute('src', reader.result);
        previewImage.setAttribute('class', 'preview-img'); // Agrega una clase CSS para controlar el tamaño de la imagen
      });
      reader.readAsDataURL(file);
      previewContainer.appendChild(previewImage);
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
        if (cursoValue === "curso1") {
            var option1 = document.createElement("option");
            option1.text = "Fundamentos de Organización de las TIC";
            option1.value = "asignatura1";
            asignaturaSelect.add(option1);

            var option2 = document.createElement("option");
            option2.text = "Fundamentos Físicos de la Informática II";
            option2.value = "asignatura2";
            asignaturaSelect.add(option2);

            var option3 = document.createElement("option");
            option3.text = "Fundamentos Matemáticos de la Informática I";
            option3.value = "asignatura3";
            asignaturaSelect.add(option3);

            var option4 = document.createElement("option");
            option4.text = "Fundamentos Matemáticos de la Informática II";
            option4.value = "asignatura4";
            asignaturaSelect.add(option4);

            var option5 = document.createElement("option");
            option5.text = "Introducción a la Ingeniería Informática";
            option5.value = "asignatura5";
            asignaturaSelect.add(option5);

            var option6 = document.createElement("option");
            option6.text = "Modelos de Computación";
            option6.value = "asignatura6";
            asignaturaSelect.add(option6);

            var option7 = document.createElement("option");
            option7.text = "Programación I";
            option7.value = "asignatura7";
            asignaturaSelect.add(option7);

            var option8 = document.createElement("option");
            option8.text = "Programación II";
            option8.value = "asignatura8";
            asignaturaSelect.add(option8);

            var option9 = document.createElement("option");
            option9.text = "Claves de Historia Contemporánea";
            option9.value = "asignatura9";
            asignaturaSelect.add(option9);
        } else if (cursoValue === "curso2") {
            var option1 = document.createElement("option");
            option1.text = "Estadística";
            option1.value = "asignatura1";
            asignaturaSelect.add(option1);

            var option2 = document.createElement("option");
            option2.text = "Análisis de los Estados Financieros";
            option2.value = "asignatura2";
            asignaturaSelect.add(option2);

            var option3 = document.createElement("option");
            option3.text = "Arquitectura de Ordenadores";
            option3.value = "asignatura3";
            asignaturaSelect.add(option3);

            var option4 = document.createElement("option");
            option4.text = "Bases de Datos I";
            option4.value = "asignatura4";
            asignaturaSelect.add(option4);

            var option5 = document.createElement("option");
            option5.text = "Bases de Datos II";
            option5.value = "asignatura5";
            asignaturaSelect.add(option5);

            var option6 = document.createElement("option");
            option6.text = "Gestión Financiera";
            option6.value = "asignatura6";
            asignaturaSelect.add(option6);

            var option7 = document.createElement("option");
            option7.text = "Metodología y Tecnología de la Programación";
            option7.value = "asignatura7";
            asignaturaSelect.add(option7);

            var option8 = document.createElement("option");
            option8.text = "Redes de Ordenadores I";
            option8.value = "asignatura8";
            asignaturaSelect.add(option8);

            var option9 = document.createElement("option");
            option9.text = "Redes de Ordenadores II";
            option9.value = "asignatura9";
            asignaturaSelect.add(option9);

            var option10 = document.createElement("option");
            option10.text = "Sistemas Operativos";
            option10.value = "asignatura10";
            asignaturaSelect.add(option10);
        } else if (cursoValue === "curso3") {
            var option1 = document.createElement("option");
            option1.text = "Administración de Sistemas de Información";
            option1.value = "asignatura1";
            asignaturaSelect.add(option1);

            var option2 = document.createElement("option");
            option2.text = "Gestión Operativa de la Empresa TIC";
            option2.value = "asignatura2";
            asignaturaSelect.add(option2);

            var option3 = document.createElement("option");
            option3.text = "Infraestructuras de Sistemas de Información";
            option3.value = "asignatura3";
            asignaturaSelect.add(option3);

            var option4 = document.createElement("option");
            option4.text = "Ingeniería del Software";
            option4.value = "asignatura4";
            asignaturaSelect.add(option4);

            var option5 = document.createElement("option");
            option5.text = "Inteligencia Artificial e Ingeniería del Conocimiento";
            option5.value = "asignatura5";
            asignaturaSelect.add(option5);

            var option6 = document.createElement("option");
            option6.text = "Programación en Entornos Distribuidos";
            option6.value = "asignatura6";
            asignaturaSelect.add(option6);

            var option7 = document.createElement("option");
            option7.text = "Proyectos de Sistemas de Información";
            option7.value = "asignatura7";
            asignaturaSelect.add(option7);

            var option8 = document.createElement("option");
            option8.text = "Sistemas de Información en la Empresa I";
            option8.value = "asignatura8";
            asignaturaSelect.add(option8);

            var option9 = document.createElement("option");
            option9.text = "Sistemas de Información para la Dirección Estratégica";
            option9.value = "asignatura9";
            asignaturaSelect.add(option9);
        } else if (cursoValue === "curso4") {
            var option1 = document.createElement("option");
            option1.text = "Doctrina Social de la Iglesia";
            option1.value = "asignatura1";
            asignaturaSelect.add(option1);

            var option2 = document.createElement("option");
            option2.text = "Hombre y Mundo Moderno";
            option2.value = "asignatura2";
            asignaturaSelect.add(option2);

            var option3 = document.createElement("option");
            option3.text = "Recursos Humanos en las Empresas TIC";
            option3.value = "asignatura3";
            asignaturaSelect.add(option3);

            var option4 = document.createElement("option");
            option4.text = "Seguridad Informática y Protección de Datos";
            option4.value = "asignatura4";
            asignaturaSelect.add(option4);

            var option5 = document.createElement("option");
            option5.text = "Sistemas Web I";
            option5.value = "asignatura5";
            asignaturaSelect.add(option5);

            var option6 = document.createElement("option");
            option6.text = "Sistemas Web II";
            option6.value = "asignatura6";
            asignaturaSelect.add(option6);

            var option7 = document.createElement("option");
            option7.text = "Trabajo de Fin de Grado";
            option7.value = "asignatura7";
            asignaturaSelect.add(option7);
        }
    } else if (carreraValue === "ADE") {
        if (cursoValue === "curso1") {
            var option1 = document.createElement("option");
            option1.text = "adex";
            option1.value = "asignatura1";
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
