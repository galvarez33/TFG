# Usa la imagen base con soporte para GPU y Python 3.8
FROM python:3.8
# Establece el directorio de trabajo en /flask
WORKDIR /flask

# Copia el código necesario al contenedor
COPY app/ /flask/app/

# Instala las dependencias necesarias para Tesseract OCR
RUN apt-get update \
    && apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia el resto de los archivos
COPY app/main.py /flask/app/
COPY app/requirements.txt /flask/app/

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r /flask/app/requirements.txt

# Expone el puerto 443 para que Flask pueda ser accedido desde fuera del contenedor
EXPOSE 443

# Comando para ejecutar la aplicación cuando se inicie el contenedor
CMD python /flask/app/main.py

