import numpy as np
import pickle
import re
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from keras.optimizers import Adam

# Lista de palabras comunes en español que quieres eliminar
palabras_comunes = ['el', 'la', 'los', 'las', 'en', 'un', 'una', 'unos', 'unas', 'y', 'o', 'pero', 'si', 'no', 'por', 'para',
    'es', 'son', 'de', 'del', 'al', 'con', 'se', 'lo', 'a', 'más', 'como', 'su', 'sus', 'tu', 'tus', 'nuestro', 'nuestra',
    'nuestros', 'nuestras', 'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas', 'esto', 'eso', 'estas',
    'estos', 'aquel', 'aquella', 'aquellos', 'aquellas', 'porque', 'para', 'entre', 'desde', 'hasta', 'cuando', 'donde',
    'cómo', 'qué', 'quiénes', 'cuál', 'cuáles', 'ser', 'estar', 'tener', 'hacer', 'poder', 'decir', 'ir', 'ver', 'saber',
    'me', 'te', 'nos', 'os', 'se', 'mi', 'mis', 'tu', 'tus', 'su', 'sus', 'nuestro', 'nuestra', 'nuestros', 'nuestras',
    'mío', 'tuyo', 'suyo', 'nuestro', 'nuestros', 'suyos', 'suyas', 'él', 'ella', 'ellos', 'ellas', 'esto', 'ese', 'eso',
    'estos', 'estas', 'aquí', 'ahí', 'allí', 'allá', 'cuánto', 'cuánta', 'cuántos', 'cuántas', 'mucho', 'mucha', 'muchos',
    'muchas', 'poco', 'poca', 'pocos', 'pocas', 'algo', 'algún', 'alguna', 'algunos', 'algunas', 'varios', 'varias', 'todo',
    'toda', 'todos', 'todas', 'ningún', 'ninguna', 'ningunos', 'ningunas', 'cualquier', 'cualesquiera', 'alguno', 'algunos',
    'alguna', 'algunas', 'ninguno', 'ninguna', 'ningunos', 'ningunas', 'otro', 'otros', 'otra', 'otras', 'mismo', 'misma',
    'mismos', 'mismas', 'tan', 'tanto', 'tantos', 'tanta', 'tantas', 'más', 'menos', 'bastante', 'bastantes', 'demasiado',
    'demasiados', 'demasiada', 'demasiadas', 'todo', 'nada', 'alguien', 'nadie', 'cada', 'cual', 'cuales', 'ambos', 'ambas',
    'mucho', 'poco', 'vario', 'varia', 'tantos', 'tantas', 'demás', 'otro', 'otra', 'otros', 'otras', 'mismo', 'misma',
    'mismos', 'mismas', 'tan', 'tanta', 'tantos', 'tantas', 'tanto', 'poca', 'pocos', 'pocas', 'bastante', 'bastantes',
    'demasiado', 'demasiados', 'demasiada', 'demasiadas', 'ninguno', 'ninguna', 'nada', 'alguien', 'nadie', 'algo', 'ningún',
    'ninguna', 'ningunos', 'ningunas', 'cualquier', 'cualesquiera', 'cualquiera', 'cualesquiera', 'cualquier', 'cualesquiera',
    'aquel', 'aquella', 'aquello', 'aquellos', 'aquellas', 'todos', 'todas', 'uno', 'una', 'unos', 'unas', 'sí', 'no',
    'si', 'como', 'muy', 'bien', 'mal', 'aunque', 'porque', 'como', 'si', 'no', 'pero', 'o', 'sino', 'aunque', 'a', 'con',
    'sin', 'en', 'durante', 'hasta', 'según', 'para', 'cómo', 'cuándo', 'dónde', 'cuál', 'cuáles', 'qué', 'quién', 'quiénes',
    'cuánto', 'cuántos', 'cuánta', 'cuántas', 'por qué', 'para qué', 'con qué', 'con quién', 'a qué', 'de qué', 'cuál es', 'qué es',
    'quién es', 'quién era', 'cuál era', 'qué significa', 'cuál significa', 'cuándo es', 'cómo es', 'dónde está', 'por qué es',
    'qué hay', 'cuántos son', 'cuántas son', 'the', 'and', 'or', 'but', 'if', 'is', 'are', 'am', 'i', 'you', 'he', 'she', 'it',
    'we', 'they', 'this', 'that', 'these', 'those', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'a', 'an', 'in', 'on', 'at',
    'to', 'with', 'from', 'by', 'of', 'for', 'about', 'as', 'be', 'have', 'do', 'can', 'could', 'will', 'would', 'shall', 'should',
    'may', 'might', 'must', 'here', 'there', 'where', 'when', 'why', 'how', 'what', 'which', 'who', 'whom', 'whose', 'this', 'that',
    'these', 'those', 'some', 'any', 'few', 'many', 'several', 'more', 'most', 'all', 'none', 'each', 'every', 'both', 'either',
    'neither', 'no', 'not', 'nor', 'so', 'too', 'very', 'just', 'now', 'then', 'since', 'while', 'before', 'after', 'during',
    'between', 'among', 'against', 'under', 'over', 'through', 'with', 'without', 'throughout', 'along', 'beside', 'amongst',
    'upon', 'within', 'toward', 'against', 'across', 'behind', 'among', 'beyond', 'above', 'below', 'near', 'far', 'inside',
    'outside', 'into', 'onto', 'up', 'down', 'forward', 'backward', 'right', 'left', 'at', 'by', 'with', 'about', 'against',
    'between', 'for', 'during', 'from', 'in', 'into', 'of', 'on', 'over', 'through', 'to', 'under', 'until', 'up', 'upon', 'with',
    'within','use','used', '' ]


palabras_clave = {
    'progra_I': [
        "abstracto", "assert", "booleano", "break", "byte", "caso", "captura", "char", "clase", 
        "constante", "continuar", "defecto", "hacer", "doble", "else", "enum", "extiende", "final", 
        "finalmente", "flotante", "for", "hacia", "implementa", "importa", "instanciaDe", 
        "int", "interfaz", "largo", "nativo", "nuevo", "paquete", "privado", "protegido", 
        "público", "retorno", "short", "estático", "estrictoFp", "super", "interruptor", "sincronizado", 
        "este", "lanzar", "lanza", "transitorio", "intentar", "void", "volátil", "mientras","objeto","variable","instancia"
        ,"programa","java","polimorfismo", "virtual", "idk","jdk"
    ],
    'mates_es': [
        'variables', 'operadores', 'AND', 'OR', 'NOT', 'XOR', 'demostración', 'teorema', 'conjuntos', 'funciones', 'grafos', 
        'árboles', 'algoritmos', 'recursión', 'combinatoria', 'permutaciones', 'combinaciones', 'números', 'relaciones',"ecuaciones","unitarios","sistema" 
        'lógica', 'predicados', 'búsqueda', 'ordenamiento', 'matemáticas', 'matemática discreta', "si","entonces","infinito","conjuntos","algebra","impar","par","p","q"
    ],
    'fisica_I': [
        'física', 'cargas','mecánica', 'óptica', 'termodinámica', 'electromagnetismo', 'termodinámica', 'magnitudes', 'fuerzas', 
        'velocidad', 'energía', 'trabajo', 'leyes', 'teoría', 'electricidad', 'magnetismo', 'óptica', 'ondas', 'partículas', 
        'termodinámica', 'calor', 'temperatura', 'leyes de Newton', 'teorema de Gauss', 'ley de Faraday', 'ley de Ampère', 
        'ley de Ohm', 'ley de Coulomb', 'movimiento', 'magnitudes físicas','fuerza','cuerpo','carga','electrica'
    ]
}

def leer_archivo(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return archivo.read()

archivo_a = leer_archivo("C:/Users/gonza/Documents/IA/textos-copia/progra_I.txt")
archivo_b = leer_archivo("C:/Users/gonza/Documents/IA/textos-copia/mates_es.txt")
archivo_c = leer_archivo("C:/Users/gonza/Documents/IA/textos-copia/fisica_I.txt")


# Crear etiquetas para los datos
etiquetas_a = ['progra_I'] * len(archivo_a.split())
etiquetas_b = ['mates_es'] * len(archivo_b.split())
etiquetas_c = ['fisica_I'] * len(archivo_c.split())

# Unir los datos y etiquetas
textos = archivo_a.split() + archivo_b.split() + archivo_c.split()
etiquetas = etiquetas_a + etiquetas_b + etiquetas_c

textos_filtrados = []

for texto, etiqueta in zip(textos, etiquetas):
    texto_limpio = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]', '', texto)
    palabras = texto_limpio.split()

    for palabra in palabras:
        categoria_asignada = None
        for categoria, palabras_clave_categoria in palabras_clave.items():
            if palabra.lower() in palabras_clave_categoria:
                categoria_asignada = categoria
                break
        
        if palabra.strip() != "" and categoria_asignada is not None:
            textos_filtrados.append(palabra + "\t" + etiqueta + "\t" + categoria_asignada)

# Guardar textos filtrados en un archivo
ruta_archivo = "textos_filtrados.txt"  # Reemplaza con la ruta y nombre de archivo deseado
with open(ruta_archivo, "w", encoding="utf-8") as archivo:
    for texto_filtrado in textos_filtrados:
        archivo.write(texto_filtrado + "\n")

print("Textos filtrados guardados en el archivo:", ruta_archivo)
print(len(textos_filtrados))

tokenizer = Tokenizer()
tokenizer.fit_on_texts(textos_filtrados)
total_palabras = len(tokenizer.word_index) + 1

# Convertir textos a secuencias numéricas
secuencias = tokenizer.texts_to_sequences(textos_filtrados)


# Pad secuencias para que tengan la misma longitud
max_longitud = max([len(s) for s in secuencias])
secuencias_padded = pad_sequences(secuencias, maxlen=max_longitud, padding='post')

# Convertir etiquetas a datos categóricos
etiquetas_categoricas = np.array([0 if etiqueta == 'progra_I' else 1 if etiqueta == 'mates_es' else 2 for etiqueta in etiquetas[:15763]])

# Dividir el conjunto de datos en entrenamiento (80%) y prueba + validación (20%)
x_train, x_temp, y_train, y_temp = train_test_split(secuencias_padded, etiquetas_categoricas, test_size=0.2, random_state=42)

# Dividir el 80% de entrenamiento en datos de entrenamiento (64%) y datos de prueba (16%)
x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=42)

# Dividir el 20% de prueba + validación en datos de prueba (80%) y datos de validación (20%)
x_val, x_test, y_val, y_test = train_test_split(x_temp, y_temp, test_size=0.2, random_state=42)

# Ahora, x_train y y_train son el 64% de los datos originales para entrenamiento,
# x_test e y_test son el 16% de los datos originales para pruebas, y
# x_val e y_val son el 20% restante para validación.

# Crear el modelo
modelo = Sequential()
modelo.add(Embedding(total_palabras, 64, input_length=max_longitud))
modelo.add(LSTM(128, return_sequences=True))
modelo.add(LSTM(128))
modelo.add(Dense(64, activation='relu'))
modelo.add(Dropout(0.5))
modelo.add(Dense(3, activation='softmax'))

# Compilar el modelo

modelo.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Entrenar el modelo
historia = modelo.fit(x_train, y_train, epochs=20, batch_size=128, validation_data=(x_val, y_val))

# Evaluar el modelo
resultado = modelo.evaluate(x_test, y_test)
print("Precisión en el conjunto de prueba:", resultado[1])

# Guardar el modelo
modelo.save('modelo_y_tokenizer.h5')

# Guardar el tokenizer a un archivo
with open('tokenizer.pkl', 'wb') as tokenizer_file:
    pickle.dump(tokenizer, tokenizer_file)

print("Métricas de entrenamiento:")
print("Precisión:", historia.history['accuracy'][-1])
print("Pérdida:", historia.history['loss'][-1])

resultado_test = modelo.evaluate(x_test, y_test)
print("Métricas en el conjunto de prueba:")
print("Precisión:", resultado_test[1])
print("Pérdida:", resultado_test[0])
