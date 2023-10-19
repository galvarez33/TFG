from model import create_model
from dataset_loader import train_images, train_text_sequences, train_labels

# Parámetros
vocab_size = 1000
max_sequence_length = 20

# Crear y compilar el modelo
model = create_model(vocab_size, max_sequence_length)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Entrenar el modelo
model.fit([train_images, train_text_sequences], train_labels, epochs=10, batch_size=4)
