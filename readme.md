# Práctica con Estudiantes CEU

## Descripción del Proyecto
Práctica con Estudiantes CEU es una plataforma web diseñada para facilitar la interacción entre estudiantes, permitiéndoles publicar dudas y recibir respuestas de otros compañeros. El proyecto está centrado en la colaboración y el intercambio de conocimientos dentro de la comunidad educativa.

## Características Principales
- **Publicación de Dudas:** Los usuarios pueden publicar sus dudas en diversas asignaturas para obtener ayuda de otros estudiantes.
- **Respuestas Colaborativas:** Facilita la colaboración entre estudiantes al permitir que respondan las dudas planteadas por otros.
- **Integración de Inteligencia Artificial:** Incorpora dos modelos de IA preentrenados:
    - `modelo.h5`: Detecta la presencia de texto en imágenes.
    - `text_classifier.joblib`: Clasifica las dudas en tres asignaturas distintas.

## Tecnologías Utilizadas
El proyecto utiliza diversas tecnologías para su correcto funcionamiento. A continuación, se enumeran algunas de ellas:
- Flask: Marco de aplicación web en Python.
- MongoDB: Base de datos NoSQL para almacenar datos de manera eficiente.
- Python: Lenguaje de programación principal del proyecto.
- Docker: Plataforma para facilitar la creación y ejecución de aplicaciones en contenedores.
- AWS: Servicios en la nube para alojar y ejecutar la aplicación de manera escalable.

## Instrucciones de Ejecución en LOCAL
1. Clona este repositorio en tu máquina local.
    ```bash
    git clone https://github.com/galvarez33/TFG.git
    ```

2. Accede al directorio del proyecto.
    ```bash
    cd TFG  
    ```

3. Instalamos Python y pip (Linux).
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip
    
    ```
4. Instalamos los requisitos.
    ```bash
    pip install -r app/requirements.txt    
    ```
5. Ejecutamos el servidor
    ```bash
    python app/main.py    
    ```
4. Abre tu navegador y visita [https://localhost:443](https://localhost:443) para acceder a la aplicación.

## Instrucciones de Despliegeue con Docker en AWS EC2

1. levanta una intancia, yo uso la t2.micro de la capa gratuita, maquina Linux.

2. Mueve tu proyecto dentro de la maquina, con erramientas como FileZilla mediante ssh puerto 22.

3. accedemos al directorio del proyecto 
    ```bash
        cd proyecto/flask  
    ```
4. construimos la imagen del docker, ejemplo: 
    ```bash
        sudo docker build -t ec2-flask:v1.https -f Dockerfile .
    ```
5. activamos el contenedor a partid de la imagen creada, ejemplo: 
    ```bash
        sudo docker run -d -p 443:443 ec2-flask:v1.https .
    ```
6. Abre tu navegador y visita [https://ip_publica_de_instancia:443](https://ips:443) para acceder a la aplicación. o al nombre de dominio asociado
   


## OpenSource
¡Contribuciones son bienvenidas! Si deseas mejorar este proyecto, siéntete libre de realizar un fork y abrir un pull request. Agradecemos tu ayuda para hacer de Práctica con Estudiantes CEU una plataforma aún mejor.

## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para obtener más detalles.
