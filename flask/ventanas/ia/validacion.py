import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import base64
from PIL import Image
from io import BytesIO

def detectar_texto_en_imagen(imagen_base64):
    # Decodificar la imagen desde Base64
    imagen_bytes = base64.b64decode(imagen_base64)
    imagen = Image.open(BytesIO(imagen_bytes))
    imagen = imagen.convert('RGB')

    # Ruta del modelo entrenado
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_modelo = os.path.join(script_dir, '..', 'modelo.h5')

    # Cargar el modelo
    modelo = load_model(ruta_modelo)

    # Preprocesar la imagen
    img = imagen.resize((150, 150))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x /= 255

    prediccion = modelo.predict(x)

    if prediccion.shape[1] == 1:
        return prediccion[0][0] > 0.5
    else:
        return prediccion[0][1] > prediccion[0][0]