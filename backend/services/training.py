from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import numpy as np
from services.database import fetch_training_data

def train_model():
    # Fetch data
    intents, examples = fetch_training_data()
    
    # Log raw data
    print("=== Datos obtenidos de la base de datos ===")
    print("Intents:", intents)
    print("Examples:", examples)
    
    # Preprocess texts and labels
    print("\n=== Procesando datos para entrenamiento ===")
    texts = [example['text'] for example in examples]
    labels = [
        intent['name']
        for intent in intents
        for example in examples
        if example['intent_id'] == intent['id']
    ]
    
    print("Textos (primeros 5):", texts[:5])
    print("Etiquetas (primeros 5):", labels[:5])

    if not texts or not labels:
        print("\nError: No se encontraron textos o etiquetas para el entrenamiento.")
        return

    # Tokenize texts
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    padded_sequences = pad_sequences(sequences, padding='post')

    print("\n=== Secuencias procesadas ===")
    print("Primeras 5 secuencias:", padded_sequences[:5])
    print(f"Número total de palabras únicas: {len(tokenizer.word_index)}")

    # Encode labels
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)

    print("\n=== Etiquetas codificadas ===")
    print("Primeras 5 etiquetas codificadas:", labels_encoded[:5])
    print(f"Clases únicas: {list(label_encoder.classes_)}")

    # Build the model
    model = Sequential([
        Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=16),
        GlobalAveragePooling1D(),
        Dense(16, activation='relu'),
        Dense(len(label_encoder.classes_), activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Training
    print("\n=== Iniciando entrenamiento ===")
    print(f"Datos de entrada: {len(padded_sequences)} ejemplos, {len(tokenizer.word_index)} palabras únicas.")
    history = model.fit(padded_sequences, np.array(labels_encoded), epochs=10, batch_size=16, verbose=1)

    # Log training results
    print("\n=== Entrenamiento completado ===")
    print(f"Loss final: {history.history['loss'][-1]}")
    print(f"Accuracy final: {history.history['accuracy'][-1]}")

    # Save model and tokenizer
    model.save('model/chatbot_model.h5')
    print("\nModelo guardado en: model/chatbot_model.h5")

    with open('model/tokenizer.json', 'w') as f:
        f.write(tokenizer.to_json())
    print("Tokenizador guardado en: model/tokenizer.json")

    with open('model/label_encoder.npy', 'wb') as f:
        np.save(f, label_encoder.classes_)
    print("Codificador de etiquetas guardado en: model/label_encoder.npy")

if __name__ == "__main__":
    print("Ejecutando el entrenamiento...")
    train_model()
