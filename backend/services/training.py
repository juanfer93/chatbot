from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import numpy as np
from .database import fetch_training_data

def train_model():
    intents, examples = fetch_training_data()

    print(f"Intents: {intents}")
    print(f"Examples: {examples}")

    texts = [example['text'] for example in examples]
    labels = [intent['name'] for intent in intents for example in examples if example['intent_id'] == intent['id']]

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    padded_sequences = pad_sequences(sequences, padding='post')

    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)

    model = Sequential([
        Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=16),
        GlobalAveragePooling1D(),
        Dense(16, activation='relu'),
        Dense(len(label_encoder.classes_), activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    print("Comenzando el entrenamiento...")

    # Entrenamiento con verbose=1 para ver la salida estándar
    history = model.fit(padded_sequences, np.array(labels_encoded), epochs=10, batch_size=16, verbose=1)

    # Al finalizar, imprime el resultado final
    print(f"\nEntrenamiento completado. Resultados finales: ")
    print(f"Loss: {history.history['loss'][-1]}")
    print(f"Accuracy: {history.history['accuracy'][-1]}")

    model.save('model/chatbot_model.h5')

    with open('model/tokenizer.json', 'w') as f:
        f.write(tokenizer.to_json())

    with open('model/label_encoder.npy', 'wb') as f:
        np.save(f, label_encoder.classes_)
