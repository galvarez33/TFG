import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

# Ruta del modelo entrenado
ruta_modelo = 'modelo.h5'

# Cargar el modelo
modelo = load_model(ruta_modelo)

# Ruta de la imagen que deseas probar
ruta_imagen = '/mnt/c/Users/gonza/Downloads/imagen1.png'

# Cargar y preprocesar la imagen
img = image.load_img(ruta_imagen, target_size=(150, 150))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x /= 255

# Realizar la predicción
prediccion = modelo.predict(x)

# Imprimir la predicción
if prediccion[0][0] > prediccion[0][1]:
    print('\nLa imagen NO tiene texto.\n')
else:
    print('\nLa imagen TIENE texto.\n')
