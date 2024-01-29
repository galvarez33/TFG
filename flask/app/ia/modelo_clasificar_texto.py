from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os

class TextClassifier:
    def __init__(self, alpha=1.0, max_features=None):
        # Define el modelo y el preprocesamiento de texto
        self.model = make_pipeline(CountVectorizer(max_features=max_features), MultinomialNB(alpha=alpha))



    def train_and_evaluate(self, data, labels):
        # Divide los datos en conjunto de entrenamiento (80%) y prueba (20%)
        X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

        # Entrenar el modelo solo con el conjunto de entrenamiento
        self.model.fit(X_train, y_train)

        # Evaluar el modelo en el conjunto de prueba
        y_pred = self.model.predict(X_test)




        # Imprimir métricas
        print("Métricas en el conjunto de prueba:")
        print(classification_report(y_test, y_pred))
        print("Matriz de confusión:")
        print(confusion_matrix(y_test, y_pred))
        print("Accuracy:", accuracy_score(y_test, y_pred))

        # Validación cruzada para obtener métricas más robustas
        cv_scores = cross_val_score(self.model, data, labels, cv=5)
        print("\nMétricas de Validación Cruzada:")
        print("Accuracy Promedio:", cv_scores.mean())
        print("Desviación Estándar de Accuracy:", cv_scores.std())

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
    directorio_actual = os.path.dirname(os.path.abspath(__file__))

    # Supongamos que tienes datos de tres asignaturas (matematicas, programacion, fisica)
    ruta_mates_data = os.path.join(directorio_actual, 'datos_clasificador', 'mates_es.txt')
    ruta_progra_data = os.path.join(directorio_actual, 'datos_clasificador', 'progra_I.txt')
    ruta_fisica_data = os.path.join(directorio_actual, 'datos_clasificador', 'fisica_I.txt')

    # Ahora puedes usar las rutas
    mates_data = open(ruta_mates_data, encoding='utf-8').readlines()
    progra_data = open(ruta_progra_data, encoding='utf-8').readlines()
    fisica_data = open(ruta_fisica_data, encoding='utf-8').readlines()

    # Concatenar los datos y etiquetas
    data = mates_data + progra_data + fisica_data
    labels = ['Fundamentos Matemáticos de la Informática I'] * len(mates_data) + ['Programación I'] * len(progra_data) + ['Fundamentos Físicos de la Informática I'] * len(fisica_data)

   

    classifier = TextClassifier(alpha=0.1,max_features=30000)
    print(len(data))

    # Entrenar el modelo con el 80% de los datos y evaluarlo en el 20% restante
    classifier.train_and_evaluate(data, labels)

    # Guardar el modelo entrenado
    classifier.save_model('text_classifier_model.joblib')

    # Probar la predicción
    new_text = "programacion orientada a objetos"
    prediction = classifier.predict(new_text)
    print(f"\nLa asignatura del texto es: {prediction}")
    