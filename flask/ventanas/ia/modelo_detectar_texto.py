import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.metrics import BinaryAccuracy, AUC, Precision, Recall
from sklearn.metrics import roc_auc_score, precision_recall_fscore_support

# Ruta de la carpeta raíz del conjunto de datos
carpeta_raiz = r"C:\\Users\\gonza\\Documents\\IA\\archive\\dataset"

# Parámetros para preprocesamiento y entrenamiento
altura, ancho = 150, 150  # Dimensiones de las imágenes
batch_size = 32

# Preprocesamiento de datos con ImageDataGenerator
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

# Crear generadores de datos
train_generator = datagen.flow_from_directory(
    os.path.join(carpeta_raiz, "train"),
    target_size=(altura, ancho),
    batch_size=batch_size,
    class_mode='binary',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    os.path.join(carpeta_raiz, "train"),
    target_size=(altura, ancho),
    batch_size=batch_size,
    class_mode='binary',
    subset='validation'
)

# Generador de datos para la carpeta de prueba
test_generator = datagen.flow_from_directory(
    os.path.join(carpeta_raiz, "test"),
    target_size=(altura, ancho),
    batch_size=batch_size,
    class_mode='binary'
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
    Dense(1, activation='sigmoid')
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

# Evaluación del conjunto de prueba
test_metrics = model.evaluate(test_generator)
print("Métricas del conjunto de prueba:")
print("Loss:", test_metrics[0])
print("Binary Accuracy:", test_metrics[1])
print("Recall:", test_metrics[2])
print("Precision:", test_metrics[3])
print("AUC:", test_metrics[4])

# Evaluación del conjunto de validación
validation_metrics = model.evaluate(validation_generator)
print("\nMétricas del conjunto de validación:")
print("Loss:", validation_metrics[0])
print("Binary Accuracy:", validation_metrics[1])
print("Recall:", validation_metrics[2])
print("Precision:", validation_metrics[3])
print("AUC:", validation_metrics[4])

# Guardar el modelo
model.save('modelo.h5')
