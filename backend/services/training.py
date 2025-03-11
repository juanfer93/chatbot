import os
import sys
import json
from pathlib import Path
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
from prepare_data import prepare_training_data  

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
MODEL_DIR = BASE_DIR / 'model'
os.makedirs(MODEL_DIR, exist_ok=True)

re_normalize = re.compile(r"[^a-záéíóúüñ¿?¡!.,\s]")
re_whitespace = re.compile(r"\s+")

def preprocess_text(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8")
    text = re_normalize.sub("", text)
    text = re_whitespace.sub(" ", text).strip()
    return text

def train_model():
    training_data = prepare_training_data()
    texts = [preprocess_text(item['text']) for item in training_data]
    labels = [item['intent'] for item in training_data]

    print("=== Datos obtenidos ===")
    print("Textos (primeros 5):", texts[:5])
    print("Etiquetas (primeros 5):", labels[:5])

    if not texts or not labels:
        print("\nError: No se encontraron textos o etiquetas para el entrenamiento.")
        return

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)

    sequences_lengths = [len(seq) for seq in sequences]
    max_length = int(np.percentile(sequences_lengths, 95))
    print(f"\nLongitud máxima ajustada: {max_length}")

    padded_sequences = pad_sequences(sequences, padding='post', maxlen=max_length)

    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)

    print("\n=== Secuencias procesadas ===")
    print("Primeras 5 secuencias:", padded_sequences[:5])
    print(f"Número total de palabras únicas: {len(tokenizer.word_index)}")

    print("\n=== Etiquetas codificadas ===")
    print("Primeras 5 etiquetas codificadas:", labels_encoded[:5])
    print(f"Clases únicas: {list(label_encoder.classes_)}")

    model = Sequential([
        Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=32, input_length=padded_sequences.shape[1]),
        GlobalAveragePooling1D(),
        Dropout(0.3),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dropout(0.3),
        Dense(len(label_encoder.classes_), activation='softmax')
    ])

    optimizer = Adam(learning_rate=0.001)
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    print("\n=== Iniciando entrenamiento ===")
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    history = model.fit(padded_sequences, np.array(labels_encoded), epochs=50, batch_size=16, verbose=1, callbacks=[early_stopping])
    print("\n=== Entrenamiento completado ===")
    print(f"Loss final: {history.history['loss'][-1]}")
    print(f"Accuracy final: {history.history['accuracy'][-1]}")

    model.save(MODEL_DIR / 'chatbot_model', save_format="tf")
    print("\nModelo guardado en:", MODEL_DIR / "chatbot_model.h5")

    with open(MODEL_DIR / 'tokenizer.json', 'w') as f:
        f.write(tokenizer.to_json())
    print("Tokenizador guardado en:", MODEL_DIR / "tokenizer.json")

    with open(MODEL_DIR / 'label_encoder.npy', 'wb') as f:
        np.save(f, label_encoder.classes_)
    print("Codificador de etiquetas guardado en:", MODEL_DIR / "label_encoder.npy")

    with open(MODEL_DIR / 'max_lenght.json', 'w') as f:
        json.dump({"max_length": max_length}, f)
    print("Longitud máxima guardada en:", MODEL_DIR / "max_length.json")

if __name__ == "__main__":
    print("Ejecutando el entrenamiento...")
    train_model()