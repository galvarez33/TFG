import os
import cv2
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd

def load_images(folder_path, num_images=20):
    images = []
    image_files = os.listdir(folder_path)[:num_images]
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        image = cv2.imread(image_path)
        # Normalizar y cambiar el tamaño de la imagen según sea necesario
        # image = preprocess_image(image)
        images.append(image)
    return np.array(images)

def load_text_sequences(file_path, num_samples=20):
    with open(file_path, 'r') as file:
        descriptions = file.readlines()[:num_samples]
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(descriptions)
    text_sequences = tokenizer.texts_to_sequences(descriptions)
    text_sequences = pad_sequences(text_sequences, maxlen=max_sequence_length)
    return text_sequences

def load_labels(file_path, num_samples=20):
    labels_df = pd.read_csv(file_path)
    labels = labels_df['label'].values[:num_samples]
    return labels

# Cargar datos
num_images = 20
max_sequence_length = 20

train_images = load_images('dataset/images_train', num_images)
train_text_sequences = load_text_sequences('dataset/descriptions_train.txt', num_images)
train_labels = load_labels('dataset/labels_train.csv', num_images)
