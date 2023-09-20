# Usar una imagen base de Python
FROM python:3.8

# Establecer el directorio de trabajo en la raíz de la aplicación
WORKDIR /app

# Copiar el archivo de requisitos y los archivos de la aplicación a la imagen
COPY requirements.txt requirements.txt
COPY . .

# Instalar las dependencias
RUN pip install -r requirements.txt

# Exponer el puerto en el que se ejecutará la aplicación Flask
EXPOSE 5001

# Comando para ejecutar la aplicación cuando se inicie el contenedor
CMD ["python", "app.py"]
