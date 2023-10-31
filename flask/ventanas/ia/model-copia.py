import os
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, LSTM, concatenate, Dense
from tensorflow.keras.metrics import Accuracy, Recall, Precision, AUC

# Parámetros para preprocesamiento y entrenamiento
max_text_length = 100  # Ajusta la longitud máxima del texto según tus datos
vocab_size = 10000  # Ajusta el tamaño del vocabulario según tus datos
embedding_dim = 128  # Ajusta la dimensión de embedding según tus datos
batch_size = 32

# Datos de texto preprocesados (ajusta estos datos según tus necesidades)
train_texts = np.random.randint(0, vocab_size, size=(1000, max_text_length))
validation_texts = np.random.randint(0, vocab_size, size=(200, max_text_length))

# Construcción del modelo RNN para el texto
input_text = Input(shape=(max_text_length,))
embedding_layer = Embedding(input_dim=vocab_size, output_dim=embedding_dim)(input_text)
lstm_layer = LSTM(128)(embedding_layer)

# Construcción del modelo CNN para las imágenes (se mantiene igual)
# ...

# Fusiona las salidas de la rama de imágenes y texto
merged = concatenate([model_img.output, lstm_layer])

output = Dense(4, activation='softmax')(merged)  # 4 unidades de salida para 4 clases con función de activación softmax

# Compilación del modelo
model = Model(inputs=[model_img.input, input_text], outputs=output)
metrics = [Accuracy(), Recall(), Precision(), AUC()]
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=metrics)

# Entrenamiento del modelo
model.fit(
    [train_generator, train_texts],
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=7,
    validation_data=([validation_generator, validation_texts],
                     validation_labels),  # Ajusta según tus datos
    validation_steps=validation_generator.samples // batch_size
)

# Calcular las predicciones en el conjunto de validación
y_pred = model.predict([validation_generator, validation_texts])
y_true = validation_generator.classes  # Las etiquetas verdaderas del conjunto de validación

# Guardar el modelo
model.save('modelo-combinado.h5')
