import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing.sequence import pad_sequences
import re


from tensorflow.keras.models import load_model
import pytesseract
from PIL import Image

class ValidadorTextoImagen:
    def __init__(self, modelo_path, tokenizer_path, max_longitud):
        self.modelo = load_model(modelo_path)
        self.tokenizer = self.load_tokenizer(tokenizer_path)
        self.max_longitud = max_longitud

    def load_tokenizer(self, tokenizer_path):
        try:
            with open(tokenizer_path, 'rb') as tokenizer_file:
                tokenizer = pickle.load(tokenizer_file)
            return tokenizer
        except Exception as e:
            # Manejar la excepción, por ejemplo, usando un tokenizer predeterminado
            print(f"Error al cargar el tokenizer: {e}")
            # Puedes crear un tokenizer predeterminado o levantar una excepción según tus necesidades
            # Ejemplo: 
            # raise Exception("No se pudo cargar el tokenizer")

    def preprocesar_texto(self, texto):
        if texto is None:
            return ""
        else:
            # Utilizar expresiones regulares para eliminar números y caracteres especiales
            texto_limpio = re.sub(r'[^a-zA-ZáóéúÁÉÍÓÚüÜñÑ\s]', '', texto)
            return " ".join(text_to_word_sequence(texto_limpio.lower()))

    def predecir_texto_en_imagen(self, ruta_imagen):
        # Leer la imagen
        texto_extraido = pytesseract.image_to_string(Image.open(ruta_imagen))
        

        # Preprocesar el texto (si es necesario)
        texto_procesado = self.preprocesar_texto(texto_extraido)
        print(texto_procesado)
        # Convertir texto a secuencia numérica
        secuencia = self.tokenizer.texts_to_sequences([texto_procesado])

        # Asegurarse de que la secuencia tenga la longitud esperada (20 en este caso)
        secuencia_padded = pad_sequences(secuencia, maxlen=self.max_longitud, padding='post')

        # Hacer la predicción utilizando el modelo
        clase_predicha = self.modelo.predict(secuencia_padded)

        # La variable clase_predicha contendrá las probabilidades para cada clase (a, b, c)
        # Puedes procesar estas probabilidades según tus necesidades
        return clase_predicha

# Ejemplo de uso
if __name__ == "__main__":
    modelo_path = 'modelo_y_tokenizer.h5'  # Ruta al archivo del modelo
    tokenizer_path = 'tokenizer.pkl'  # Ruta al archivo del tokenizer
    max_longitud = 5 # Define la longitud máxima para las secuencias (reemplaza con el valor adecuado)

    
    validador = ValidadorTextoImagen(modelo_path, tokenizer_path, max_longitud)
    ruta_imagen = 'C:/Users/gonza/Downloads/imagen_progra2.jpg'
    clase_predicha = validador.predecir_texto_en_imagen(ruta_imagen)
        
    print("La clase predicha es:")
    print(clase_predicha)


'''
    for _ in range(10):
        validador = ValidadorTextoImagen(modelo_path, tokenizer_path, max_longitud)
        ruta_imagen = 'C:/Users/gonza/Downloads/imagenp.jpg'
        clase_predicha = validador.predecir_texto_en_imagen(ruta_imagen)
        
        print("La clase predicha es:")
        print(clase_predicha)'''