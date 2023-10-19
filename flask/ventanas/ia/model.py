from tensorflow.keras.layers import Input, Dense, Embedding, LSTM, Concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.applications import ResNet50

def create_model(vocab_size, max_sequence_length):
    # Entrada para imágenes
    input_image = Input(shape=(224, 224, 3))
    resnet = ResNet50(weights='imagenet', include_top=False)(input_image)
    flatten_image = tf.keras.layers.Flatten()(resnet)

    # Entrada para texto
    input_text = Input(shape=(max_sequence_length,))
    embedding_layer = Embedding(vocab_size, 100)(input_text)
    lstm_text = LSTM(256)(embedding_layer)

    # Fusionar representaciones
    merged = Concatenate()([flatten_image, lstm_text])

    # Capas adicionales para la clasificación
    dense_layer = Dense(512, activation='relu')(merged)
    output = Dense(1, activation='sigmoid')(dense_layer)

    model = Model(inputs=[input_image, input_text], outputs=output)
    return model
