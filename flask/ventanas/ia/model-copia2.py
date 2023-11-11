from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn import metrics
import joblib

class TextClassifier:
    def __init__(self):
        # Define el modelo y el preprocesamiento de texto
        self.model = make_pipeline(CountVectorizer(), MultinomialNB())

    def train(self, data, labels):
        # Divide los datos en conjunto de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

        # Entrenar el modelo
        self.model.fit(X_train, y_train)

        # Evaluar el modelo
        y_pred = self.model.predict(X_test)
        accuracy = metrics.accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy}")

    def predict(self, text):
        # Predecir la asignatura del texto dado
        prediction = self.model.predict([text])
        return prediction[0]

    def save_model(self, filename):
        # Guardar el modelo entrenado en un archivo
        joblib.dump(self.model, filename)

    def load_model(self, filename):
        # Cargar el modelo entrenado desde un archivo
        self.model = joblib.load(filename)

# Ejemplo de uso
if __name__ == "__main__":
    # Supongamos que tienes datos de tres asignaturas (math, history, science)
    math_data = open('C:/Users/gonza/Documents/IA/textos-copia/mates_es.txt', encoding='utf-8').readlines()
    history_data = open('C:/Users/gonza/Documents/IA/textos-copia/progra_I.txt', encoding='utf-8').readlines()
    science_data = open('C:/Users/gonza/Documents/IA/textos-copia/fisica_I.txt', encoding='utf-8').readlines()

    # Concatenar los datos y etiquetas
    data = math_data + history_data + science_data
    labels = ['math'] * len(math_data) + ['prog'] * len(history_data) + ['fisic'] * len(science_data)

    # Crear una instancia de la clase TextClassifier
    classifier = TextClassifier()

    # Entrenar el modelo
    classifier.train(data, labels)

    # Guardar el modelo entrenado
    classifier.save_model('text_classifier_model.joblib')

    # Para cargar el modelo en el futuro
    # classifier.load_model('text_classifier_model.joblib')

    # Probar la predicción
    new_text = "programacion orientada a obuetos man elercicio resuelto java escribir un programa que permita obtener el perimetro de un triangulo usando una clase triangulo si no se indican valores por defecto los lados del triangulo seran de y class triangulo private int lado ladob ladoc public triangulo ladoa ladob ladoc public trianguloint a int b int c ladoaa ladobb ladocc int perimetro return ladoaladobladoc i void setladoaint a ladoaa void setladobint b ladobb void setladocint c ladocc int getladoa return ladoa int getladob return ladob public class prueba a public static void mainstring args int getladoc return ladoc triangulo tinew triangulo triangulo tnew triangulo systemoutprintlntperimetro systemoutprintntperimetro tsetladoa systemoutprintlntperimetro"
    prediction = classifier.predict(new_text)
    print(f"La asignatura del texto es: {prediction}")
