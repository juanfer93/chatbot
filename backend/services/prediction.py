import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import tokenizer_from_json
import json
from services.database import save_unclassified_message, get_intent_name_by_id

model = load_model('backend/model/chatbot_model.h5')

with open('backend/model/tokenizer.json', 'r') as f:
    tokenizer_data = json.load(f)  
    tokenizer = tokenizer_from_json(json.dumps(tokenizer_data))  

with open('backend/model/label_encoder.npy', 'rb') as f:
    label_encoder = np.load(f)

def predict_intent(message):
    sequence = tokenizer.texts_to_sequences([message])
    padded_sequence = pad_sequences(sequence, padding='post', maxlen=model.input_shape[1])
    prediction = model.predict(padded_sequence)
    intent_index = np.argmax(prediction)
    return label_encoder[intent_index]

def handle_message(message):
    try:
        intent_id = predict_intent(message)
        intent_name = get_intent_name_by_id(intent_id)
        if intent_name:
            return f"Intento detectado: {intent_name}"
        else:
            save_unclassified_message(message)
            return "No se ha detectado ningún intento."
    except Exception as e:
        print(f"Error al predecir intento: {e}")
        save_unclassified_message(message)
        return "Lo siento, no entiendo esto. Lo he guardado para aprenderlo más tarde."
