import numpy as np
import pickle
import re
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense,Dropout,GRU

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
    'si', 'como', 'muy', 'bien', 'mal', 'aunque', 'porque', 'para', 'con', 'sin', 'antes', 'después', 'durante', 'fuera',
    'dentro', 'casi', 'siempre', 'nunca', 'quizás', 'tal', 'vez', 'sobre', 'bajo', 'ante', 'alrededor', 'mediante', 'tras',
    'encima', 'debajo', 'lejos', 'cerca', 'hacia', 'dónde', 'aquí', 'allí', 'ahí', 'arriba', 'abajo', 'adelante', 'atrás',
    'derecha', 'izquierda', 'cerca', 'lejos', 'pronto', 'tarde', 'ayer', 'hoy', 'mañana', 'ya', 'aún', 'todavía', 'entonces',
    'ahora', 'cuando', 'mientras', 'porque', 'como', 'si', 'no', 'pero', 'o', 'sino', 'aunque', 'a', 'con', 'sin', 'en',
    'durante', 'hasta', 'según', 'para', 'cómo', 'cuándo', 'dónde', 'cuál', 'cuáles', 'qué', 'quién', 'quiénes', 'cuánto',
    'cuántos', 'cuánta', 'cuántas', 'por qué', 'para qué', 'con qué', 'con quién', 'a qué', 'de qué', 'cuál es', 'qué es',
    'quién es', 'quién era', 'cuál era', 'qué significa', 'cuál significa', 'cuándo es', 'cómo es', 'dónde está', 'por qué es',
    'qué hay', 'cuántos son', 'cuántas son','the', 'and', 'or', 'but', 'if', 'is', 'are', 'am', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'this', 'that', 
    'these', 'those', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'a', 'an', 'in', 'on', 'at', 'to', 'with', 
    'from', 'by', 'of', 'for', 'about', 'as', 'be', 'have', 'do', 'can', 'could', 'will', 'would', 'shall', 'should', 
    'may', 'might', 'must', 'here', 'there', 'where', 'when', 'why', 'how', 'what', 'which', 'who', 'whom', 'whose', 
    'this', 'that', 'these', 'those', 'some', 'any', 'few', 'many', 'several', 'more', 'most', 'all', 'none', 'each', 
    'every', 'both', 'either', 'neither', 'no', 'not', 'nor', 'so', 'too', 'very', 'just', 'now', 'then', 'since', 
    'while', 'before', 'after', 'during', 'between', 'among', 'against', 'under', 'over', 'through', 'with', 'without', 
    'throughout', 'along', 'beside', 'amongst', 'upon', 'within', 'toward', 'against', 'across', 'behind', 'among', 
    'beyond', 'above', 'below', 'near', 'far', 'inside', 'outside', 'into', 'onto', 'up', 'down', 'forward', 'backward', 
    'right', 'left', 'at', 'by', 'with', 'about', 'against', 'between', 'for', 'during', 'from', 'in', 'into', 'of', 
    'on', 'over', 'through', 'to', 'under', 'until', 'up', 'upon', 'with', 'within','use','used', '' ]


def leer_archivo(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()[:100000]
    return lineas

archivo_a = leer_archivo("C:/Users/gonza/Documents/IA/textos/fisica_I.txt")
archivo_b = leer_archivo("C:/Users/gonza/Documents/IA/textos/matematicas_I.txt")
archivo_c = leer_archivo("C:/Users/gonza/Documents/IA/textos/progra_I.txt")

# Crear etiquetas para los datos
etiquetas_a = ['a'] * len(archivo_a)
etiquetas_b = ['b'] * len(archivo_b)
etiquetas_c = ['c'] * len(archivo_c)

# Unir los datos y etiquetas
textos = archivo_a + archivo_b + archivo_c
etiquetas = etiquetas_a + etiquetas_b + etiquetas_c

# Filtrar palabras comunes
textos_filtrados = []
for texto in textos:   
    texto_limpio = re.sub(r'[^a-zA-Z\s]', '', texto)  # Eliminar números y caracteres especiales
    palabras = texto_limpio.split()  # Tokenizar palabras utilizando espacios como delimitadores
    palabras_filtradas = [palabra for palabra in palabras if palabra.lower() not in palabras_comunes]
    texto_filtrado = ' '.join(palabras_filtradas)

    if texto_filtrado.strip() != "" and texto_filtrado not in textos_filtrados:
        textos_filtrados.append(texto_filtrado)
    
textos_sin_vacios = [texto for texto in textos if texto.strip() != ""]
# Imprimir la cantidad de textos filtrados
print(len(textos_filtrados))
print(textos_sin_vacios)


tokenizer = Tokenizer()
tokenizer.fit_on_texts(textos_sin_vacios)
total_palabras = len(tokenizer.word_index) + 1

# Convertir textos a secuencias numéricas
secuencias = tokenizer.texts_to_sequences(textos_filtrados)

# Pad secuencias para que tengan la misma longitud
max_longitud = max([len(s) for s in secuencias])
secuencias_padded = pad_sequences(secuencias, maxlen=max_longitud, padding='post')

# Convertir etiquetas a datos categóricos
etiquetas_categoricas = np.array([0 if etiqueta == 'a' else 1 if etiqueta == 'b' else 2 for etiqueta in etiquetas[:69635]])

x_train, x_test, y_train, y_test = train_test_split(secuencias_padded, etiquetas_categoricas, test_size=0.2, random_state=42)

modelo = Sequential()
modelo.add(Embedding(total_palabras, 64, input_length=max_longitud))
modelo.add(GRU(64))  # Cambiado de LSTM a GRU
modelo.add(Dense(3, activation='softmax'))

modelo.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Entrenar el modelo
historia = modelo.fit(x_train, y_train, epochs=5, batch_size=64, validation_data=(x_test, y_test))

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

    
