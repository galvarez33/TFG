# Usa la imagen base de Python 3.8
FROM python:3.8

# Establece el directorio de trabajo en /flask
WORKDIR /flask

# Copia el código necesario al contenedor
COPY ventanas/ /flask/ventanas/
COPY ventanas/main.py /flask/ventanas/
COPY ventanas/requirements.txt /flask/ventanas/

# Instala las dependencias
RUN pip install --no-cache-dir -r /flask/ventanas/requirements.txt

# Expone el puerto 5000 para que Flask pueda ser accedido desde fuera del contenedor
EXPOSE 5001

# Comando para ejecutar la aplicación cuando se inicie el contenedor
CMD ["python", "ventanas/main.py"]
