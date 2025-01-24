import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, Dropout, GlobalAveragePooling1D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import numpy as np
import re
import unicodedata
from services.database import fetch_training_data

def preprocess_text(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8")
    text = re.sub(r"[^a-záéíóúüñ¿?¡!.,\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def train_model():
    intents, examples = fetch_training_data()

    print("=== Datos obtenidos de la base de datos ===")
    print("Intents:", intents)
    print("Examples:", examples)

    print("\n=== Procesando datos para entrenamiento ===")
    texts = [preprocess_text(example['text']) for example in examples]
    labels = []
    for intent in intents:
        for example in examples:
            if example['intent_id'] == intent['id']:
                labels.append(intent['name'])
                print(f"Asociación encontrada: Intent({intent['name']}) con Example({example['text']})")

    print("Textos (primeros 5):", texts[:5])
    print("Etiquetas (primeros 5):", labels[:5])

    if not texts or not labels:
        print("\nError: No se encontraron textos o etiquetas para el entrenamiento.")
        return

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    padded_sequences = pad_sequences(sequences, padding='post')

    print("\n=== Secuencias procesadas ===")
    print("Primeras 5 secuencias:", padded_sequences[:5])
    print(f"Número total de palabras únicas: {len(tokenizer.word_index)}")

    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)

    print("\n=== Etiquetas codificadas ===")
    print("Primeras 5 etiquetas codificadas:", labels_encoded[:5])
    print(f"Clases únicas: {list(label_encoder.classes_)}")

    model = Sequential([
        Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=64, input_length=padded_sequences.shape[1]),
        GlobalAveragePooling1D(),
        Dropout(0.3),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(len(label_encoder.classes_), activation='softmax')
    ])

    optimizer = Adam(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    print("\n=== Iniciando entrenamiento ===")
    print(f"Datos de entrada: {len(padded_sequences)} ejemplos, {len(tokenizer.word_index)} palabras únicas.")

    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

    history = model.fit(padded_sequences, np.array(labels_encoded), epochs=50, batch_size=16, verbose=1, callbacks=[early_stopping])

    print("\n=== Entrenamiento completado ===")
    print(f"Loss final: {history.history['loss'][-1]}")
    print(f"Accuracy final: {history.history['accuracy'][-1]}")

    model.save('backend/model/chatbot_model.h5')
    print("\nModelo guardado en: model/chatbot_model.h5")

    with open('backend/model/tokenizer.json', 'w') as f:
        f.write(tokenizer.to_json())
    print("Tokenizador guardado en: model/tokenizer.json")

    with open('backend/model/label_encoder.npy', 'wb') as f:
        np.save(f, label_encoder.classes_)
    print("Codificador de etiquetas guardado en: model/label_encoder.npy")

if __name__ == "__main__":
    print("Ejecutando el entrenamiento...")
    train_model()