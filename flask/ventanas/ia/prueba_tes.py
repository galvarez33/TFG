
from PIL import Image
import pytesseract

# Ruta de la imagen de la que quieres extraer texto
ruta_imagen = 'C:/Users/gonza/Downloads/imagen1.png'

# Utiliza Tesseract OCR para extraer texto de la imagen
texto_extraido = pytesseract.image_to_string(Image.open(ruta_imagen))

# Imprime el texto extraído
print('Texto extraído de la imagen:')
print(texto_extraido)
