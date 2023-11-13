from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib
import pytesseract
from PIL import Image
import base64
import io

class TextClassifier:
    def __init__(self, modelo_path):
        # Define el modelo
        self.model = joblib.load(modelo_path)

    def predecir_texto_en_imagen(self, imagen_bytes):
        
        try:
            # Decodificar los bytes de la imagen y convertir a imagen PIL
            decoded_bytes = base64.b64decode(imagen_bytes)
            imagen_pil = Image.open(io.BytesIO(decoded_bytes))

            # Extraer texto de la imagen
            texto_extraido = pytesseract.image_to_string(imagen_pil)
            print(texto_extraido)
            # Convertir texto a una lista para que pueda ser utilizada por el modelo de Naive Bayes
            lista_texto = [texto_extraido]

            # Hacer la predicción utilizando el modelo de Naive Bayes
            clase_predicha = self.model.predict(lista_texto)

            return clase_predicha[0]
        except Exception as e:
            print(f"Error al procesar la imagen: {e}")
            return "Error en la predicción"

# Ejemplo de uso
if __name__ == "__main__":
    modelo_path = 'text_classifier_model.joblib'  # Ruta al archivo del modelo de Naive Bayes

    classifier = TextClassifier(modelo_path)

    # Probar la predicción con texto extraído de una imagen
    ruta_imagen = 'C:/Users/gonza/Downloads/imagenp.jpg'
    imagen_bytes = base64.b64encode(open(ruta_imagen, "rb").read()).decode("utf-8")
    clase_predicha = classifier.predecir_texto_en_imagen(imagen_bytes)

    print("La clase predicha es:")
    print(clase_predicha)
