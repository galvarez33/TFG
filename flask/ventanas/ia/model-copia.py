import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Rutas de las carpetas de imágenes
carpeta_con_texto = '/mnt/c/Users/gonza/Documents/IA/archive/dataset/texto'
carpeta_sin_texto = '/mnt/c/Users/gonza/Documents/IA/archive/dataset/notexto'
carpeta= "/mnt/c/Users/gonza/Documents/IA/archive/dataset"
# Parámetros para preprocesamiento y entrenamiento
altura, ancho = 150, 150  # Dimensiones de las imágenes
batch_size = 32
num_clases = 2

# Preprocesamiento de datos con ImageDataGenerator
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
train_generator = datagen.flow_from_directory(
    carpeta,  
    target_size=(altura, ancho),
    batch_size=batch_size,
    class_mode='binary',
    subset='training'
)
validation_generator = datagen.flow_from_directory(
    carpeta,
    target_size=(altura, ancho),
    batch_size=batch_size,
    class_mode='binary',
    subset='validation'
)

# Construcción del modelo CNN
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(altura, ancho, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(256, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(512, activation='relu'),
    Dense(num_clases, activation='softmax')
])

# Compilación del modelo
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entrenamiento del modelo
model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=5,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size
)
model.save('modelo.h5')