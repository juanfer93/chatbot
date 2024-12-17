import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import tokenizer_from_json
import json
from services.database import save_unclassified_message

model = load_model('model/chatbot_model.h5')

with open('model/tokenizer.json', 'r') as f:
    tokenizer_data = json.load(f)  
    tokenizer = tokenizer_from_json(json.dumps(tokenizer_data))  

with open('model/label_encoder.npy', 'rb') as f:
    label_encoder = np.load(f)

def predict_intent(message):
    sequence = tokenizer.texts_to_sequences([message])
    padded_sequence = pad_sequences(sequence, padding='post', maxlen=model.input_shape[1])
    prediction = model.predict(padded_sequence)
    intent_index = np.argmax(prediction)
    return label_encoder[intent_index]

def handle_message(message):
    try:
        intent = predict_intent(message)
        return f"Intento detectado: {intent}"
    except:
        save_unclassified_message(message)
        return "Lo siento, no entiendo esto. Lo he guardado para aprenderlo más tarde."
