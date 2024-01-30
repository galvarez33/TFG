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
                
                    const errorMessage = "Esta imagen no contiene texto, por favor, seleccione otra.";  
                    
                    window.location.href = `/error-texto?error=${encodeURIComponent(errorMessage)}`;
                    
                });}

            // Leer el contenido del archivo como URL
            reader.readAsDataURL(file);
        } else {
            // Mostrar un mensaje de error si el archivo no es una imagen
            const errorMessage = 'El archivo seleccionado no tiene formato de imagen png, jpg, etc.';
            previewContainer.appendChild(document.createTextNode(errorMessage));

            // Recargar la página con un mensaje de error
            const errorQueryParam = encodeURIComponent(errorMessage);
            window.location.href = `/error-texto?error=${errorQueryParam}`;
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
        // Asignaturas de primer año de ISI
    "Claves de Historia y Literatura": { carrera: "ISI", curso: "1º" },
    "Fundamentos de Organización de las TIC": { carrera: "ISI", curso: "1º" },
    "Fundamentos Físicos de la Informática I": { carrera: "ISI", curso: "1º" },
    "Fundamentos Físicos de la Informática II": { carrera: "ISI", curso: "1º" },
    "Fundamentos Matemáticos de la Informática I": { carrera: "ISI", curso: "1º" },
    "Fundamentos Matemáticos de la Informática II": { carrera: "ISI", curso: "1º" },
    "Introducción a la Ingeniería Informática": { carrera: "ISI", curso: "1º" },
    "Modelos de Computación": { carrera: "ISI", curso: "1º" },
    "Programación I": { carrera: "ISI", curso: "1º" },
    "Programación II": { carrera: "ISI", curso: "1º" },
    
    // Asignaturas de segundo año de ISI
    "Estadística": { carrera: "ISI", curso: "2º" },
    "Análisis de los Estados Financieros": { carrera: "ISI", curso: "2º" },
    "Arquitectura de Ordenadores": { carrera: "ISI", curso: "2º" },
    "Bases de Datos I": { carrera: "ISI", curso: "2º" },
    "Bases de Datos II": { carrera: "ISI", curso: "2º" },
    "Gestión Financiera": { carrera: "ISI", curso: "2º" },
    "Metodología y Tecnología de la Programación": { carrera: "ISI", curso: "2º" },
    "Redes de Ordenadores I": { carrera: "ISI", curso: "2º" },
    "Redes de Ordenadores II": { carrera: "ISI", curso: "2º" },
    "Sistemas Operativos": { carrera: "ISI", curso: "2º" },
    
    // Asignaturas de tercer año de ISI
    "Administración de Sistemas de Información": { carrera: "ISI", curso: "3º" },
    "Gestión Operativa de la Empresa TIC": { carrera: "ISI", curso: "3º" },
    "Infraestructuras de Sistemas de Información": { carrera: "ISI", curso: "3º" },
    "Ingeniería del Software": { carrera: "ISI", curso: "3º" },
    "Inteligencia Artificial e Ingeniería del Conocimiento": { carrera: "ISI", curso: "3º" },
    "Programación en Entornos Distribuidos": { carrera: "ISI", curso: "3º" },
    "Proyectos de Sistemas de Información": { carrera: "ISI", curso: "3º" },
    "Sistemas de Información en la Empresa I": { carrera: "ISI", curso: "3º" },
    "Sistemas de Información en la Empresa II": { carrera: "ISI", curso: "3º" },
    "Sistemas de Información para la Dirección Estratégica": { carrera: "ISI", curso: "3º" },
    
    // Asignaturas de cuarto año de ISI
    "Doctrina Social de la Iglesia": { carrera: "ISI", curso: "4º" },
    "Estrategia y Política Empresarial en las Empresas TIC": { carrera: "ISI", curso: "4º" },
    "Ética y Deontología": { carrera: "ISI", curso: "4º" },
    "Recursos Humanos en las Empresas TIC": { carrera: "ISI", curso: "4º" },
    "Seguridad Informática y Protección de Datos": { carrera: "ISI", curso: "4º" },
    "Sistemas Web I": { carrera: "ISI", curso: "4º" },
    "Sistemas Web II": { carrera: "ISI", curso: "4º" },
    "Prácticas Externas": { carrera: "ISI", curso: "4º" },
    "Trabajo de Fin de Grado": { carrera: "ISI", curso: "4º" },

    "Derecho de la empresa": { carrera: "ADE", curso: "1º" },
    "Fundamentos de gestión empresarial": { carrera: "ADE", curso: "1º" },
    "Matemáticas I": { carrera: "ADE", curso: "1º" },
    "Microeconomía": { carrera: "ADE", curso: "1º" },
    "Estadística I": { carrera: "ADE", curso: "1º" },
    "Pensamiento creativo": { carrera: "ADE", curso: "1º" },
    "Claves de historia contemporánea": { carrera: "ADE", curso: "1º" },
    "Fundamentos de contabilidad financiera": { carrera: "ADE", curso: "1º" },
    "Fundamentos de Marketing": { carrera: "ADE", curso: "1º" },
    "Ética": { carrera: "ADE", curso: "1º" },
    "Herramientas para el análisis de datos": { carrera: "ADE", curso: "1º" },
    "Matemáticas II": { carrera: "ADE", curso: "2º" },
    
    // Asignaturas de segundo año de ADE
    "Doctrina social de la Iglesia": { carrera: "ADE", curso: "2º" },
    "Macroeconomía": { carrera: "ADE", curso: "2º" },
    "Estadística II": { carrera: "ADE", curso: "2º" },
    "Financiación empresarial": { carrera: "ADE", curso: "2º" },
    "Fiscalidad empresarial para la toma de decisiones": { carrera: "ADE", curso: "2º" },
    "Historia económica y de la empresa": { carrera: "ADE", curso: "2º" },
    "Contabilidad y fiscalidad en la empresa": { carrera: "ADE", curso: "2º" },
    "Dirección financiera": { carrera: "ADE", curso: "2º" },
    "Gestión de marketing": { carrera: "ADE", curso: "2º" },
    "Herramientas de análisis estadístico para la empresa": { carrera: "ADE", curso: "2º" },
    "Organización y diseño empresarial": { carrera: "ADE", curso: "2º" },
    
    // Asignaturas de tercer año de ADE
    "Análisis de estados financieros": { carrera: "ADE", curso: "3º" },
    "Contabilidad para la toma de decisiones": { carrera: "ADE", curso: "3º" },
    "Dirección de operaciones": { carrera: "ADE", curso: "3º" },
    "Política económica": { carrera: "ADE", curso: "3º" },
    "Finanzas tecnológicas": { carrera: "ADE", curso: "3º" },
    "Gestión de patrimonios y carteras": { carrera: "ADE", curso: "3º" },
    "Econometría": { carrera: "ADE", curso: "3º" },
    "Empresa y emprendimiento I": { carrera: "ADE", curso: "3º" },
    "Empresa y emprendimiento II": { carrera: "ADE", curso: "3º" },
    "Macroeconomía aplicada": { carrera: "ADE", curso: "3º" },
    "Valoración de activos financieros": { carrera: "ADE", curso: "3º" },
    "Casos de realidad empresarial": { carrera: "ADE", curso: "3º" },
    "Transformación digital de la empresa": { carrera: "ADE", curso: "3º" },
    
    // Asignaturas de cuarto año de ADE
    "Gestión de la cadena de suministro": { carrera: "ADE", curso: "4º" },
    "Deontología": { carrera: "ADE", curso: "4º" },
    "Business English": { carrera: "ADE", curso: "4º" },
    "Análisis estratégico de la empresa": { carrera: "ADE", curso: "4º" },
    "Estrategias corporativas de la empresa": { carrera: "ADE", curso: "4º" },
    "Economía para el siglo XXI": { carrera: "ADE", curso: "4º" },
    "Dirección de personas": { carrera: "ADE", curso: "4º" },
    "Trabajo Fin de Grado (ADE)": { carrera: "ADE", curso: "4º" },
    "Prácticas académicas externas": { carrera: "ADE", curso: "4º" },
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

    // Si hay información para la asignatura predicha, agrégala al desplegable
    if (infoAsignatura) {
        var option = document.createElement("option");
        option.text = asignatura;
        option.value = asignatura;
        asignaturaSelect.add(option);

        // Establece los valores de carrera y curso
        carreraSelect.value = infoAsignatura.carrera;
        cursoSelect.value = infoAsignatura.curso;
    } else {
        console.warn("No se encontró información para la asignatura: " + asignatura);
    }

    // Filtrar las asignaturas por carrera y curso
    var asignaturasFiltradas = Object.keys(asignaturasDefinidas)
        .filter(function(asignaturaKey) {
            return asignaturasDefinidas[asignaturaKey].carrera === carreraSelect.value &&
                   asignaturasDefinidas[asignaturaKey].curso === cursoSelect.value;
        });

    // Cargar las asignaturas filtradas en el desplegable
    asignaturasFiltradas.forEach(function(asignaturaKey) {
        var option = document.createElement("option");
        option.text = asignaturaKey;
        option.value = asignaturaKey;
        asignaturaSelect.add(option);
    });
}

// Llama a la función al cargar la página para mostrar todas las asignaturas
updateAsignaturas();


