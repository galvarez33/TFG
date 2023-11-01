import os
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from sklearn.preprocessing import LabelEncoder

# Ruta de la carpeta con los archivos de texto
carpeta = '/mnt/c/Users/ASUS/Documents/IA/textos'

# Leer los textos de los archivos en la carpeta
textos = []
categorias = []

for archivo in os.listdir(carpeta):
    with open(os.path.join(carpeta, archivo), 'r', encoding='utf-8') as file:
        texto = file.read()
        textos.append(texto)
        categorias.append(archivo.split('_')[0])  # El nombre del archivo se usa como categoría

# Convertir las categorías a números
label_encoder = LabelEncoder()
categorias_encoded = label_encoder.fit_transform(categorias)

# Tokenización de texto
tokenizer = Tokenizer()
tokenizer.fit_on_texts(textos)
total_palabras = len(tokenizer.word_index) + 1

# Convertir texto a secuencias numéricas
secuencias = tokenizer.texts_to_sequences(textos)

# Padding para que todas las secuencias tengan la misma longitud
max_longitud = max([len(seq) for seq in secuencias])
secuencias_padded = pad_sequences(secuencias, maxlen=max_longitud, padding='post')

# Construcción del modelo RNN
model = Sequential([
    Embedding(total_palabras, 64, input_length=max_longitud),
    LSTM(128),
    Dense(len(label_encoder.classes_), activation='softmax')  # Salida con función de activación softmax para clasificación no binaria
])

# Compilación del modelo
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Datos de entrenamiento y etiquetas
datos_entrenamiento = secuencias_padded
etiquetas = np.array(categorias_encoded)

# Entrenamiento del modelo
model.fit(datos_entrenamiento, etiquetas, epochs=10, batch_size=1)

# Guardar el modelo
model.save('modelo_texto_no_binario.h5')

# Guardar el encoder para convertir categorías a números durante la predicción
import joblib
joblib.dump(label_encoder, 'label_encoder.pkl')
