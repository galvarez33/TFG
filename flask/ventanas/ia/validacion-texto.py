from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib
import re
import pytesseract
from PIL import Image

class ValidadorTextoImagen:
    def __init__(self, modelo_path, tokenizer_path, max_longitud):
        self.modelo = self.load_model(modelo_path)
        self.tokenizer = self.load_tokenizer(tokenizer_path)
        self.max_longitud = max_longitud

    def load_model(self, modelo_path):
        try:
            model = joblib.load(modelo_path)
            return model
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")
            # Manejar la excepción según tus necesidades

    def load_tokenizer(self, tokenizer_path):
        try:
            with open(tokenizer_path, 'rb') as tokenizer_file:
                tokenizer = joblib.load(tokenizer_file)
            return tokenizer
        except Exception as e:
            print(f"Error al cargar el tokenizer: {e}")
            # Manejar la excepción según tus necesidades

    def preprocesar_texto(self, texto):
        if texto is None:
            return ""
        else:
            # Utilizar expresiones regulares para eliminar números y caracteres especiales
            texto_limpio = re.sub(r'[^a-zA-ZáóéúÁÉÍÓÚüÜñÑ\s]', '', texto)
            return " ".join(texto_limpio.lower().split())

    def predecir_texto_en_imagen(self, ruta_imagen):
        # Leer la imagen
        texto_extraido = pytesseract.image_to_string(Image.open(ruta_imagen))
        
        # Preprocesar el texto (si es necesario)
        texto_procesado = self.preprocesar_texto(texto_extraido)

        # Convertir texto a una lista para que pueda ser utilizada por el modelo de Naive Bayes
        lista_texto = [texto_procesado]

        # Hacer la predicción utilizando el modelo de Naive Bayes
        clase_predicha = self.modelo.predict(lista_texto)

        return clase_predicha

# Ejemplo de uso
if __name__ == "__main__":
    modelo_path = 'text_classifier_model.joblib'  # Ruta al archivo del modelo de Naive Bayes
    tokenizer_path = 'tokenizer.pkl'  # Ruta al archivo del tokenizer
    max_longitud = 5  # Define la longitud máxima para las secuencias (reemplaza con el valor adecuado)

    validador = ValidadorTextoImagen(modelo_path, tokenizer_path, max_longitud)
    ruta_imagen = 'C:/Users/gonza/Downloads/imagenp.jpg'
    clase_predicha = validador.predecir_texto_en_imagen(ruta_imagen)
        
    print("La clase predicha es:")
    print(clase_predicha)
