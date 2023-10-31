import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.metrics import BinaryAccuracy, AUC, Precision, Recall
from sklearn.metrics import roc_auc_score, precision_recall_fscore_support



# Rutas de las carpetas de imágenes
carpeta_con_texto = '/mnt/c/Users/gonza/Documents/IA/archive/dataset/texto'
carpeta_sin_texto = '/mnt/c/Users/ASUS/Documents/IA/archive/dataset/notexto'
carpeta= "/mnt/c/Users/ASUS/Documents/IA/archive/dataset"
# Parámetros para preprocesamiento y entrenamiento
altura, ancho = 150, 150  # Dimensiones de las imágenes
batch_size = 32

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
    Dense(256, activation='relu'),
    Dense(1, activation='sigmoid')  # 1 unidad de salida con función de activación sigmoide para clasificación binaria
])

# Compilación del modelo
metrics = ["binary_accuracy", Recall(thresholds=0.5), Precision(thresholds=0.5), AUC()]
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=metrics)

# Entrenamiento del modelo
model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=7,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size
)

# Calcular las predicciones en el conjunto de validación
y_pred = model.predict(validation_generator)
y_true = validation_generator.classes  # Las etiquetas verdaderas del conjunto de validación



# Guardar el modelo
model.save('modelo.h5')
