from pathlib import Path
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import tokenizer_from_json
import json
from services.database import save_unclassified_message, get_response_by_intent

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / 'model'

model_path = MODEL_DIR / 'chatbot_model.h5'
model = load_model(model_path)

tokenizer_path = MODEL_DIR / 'tokenizer.json'
with open(tokenizer_path, 'r') as f:
    tokenizer_data = json.load(f)
    tokenizer = tokenizer_from_json(json.dumps(tokenizer_data))

label_encoder_path = MODEL_DIR / 'label_encoder.npy'
with open(label_encoder_path, 'rb') as f:
    label_encoder = np.load(f)

def predict_intent(message):
    try:
        sequence = tokenizer.texts_to_sequences([message])
        padded_sequence = pad_sequences(sequence, padding='post', maxlen=model.input_shape[1])
        prediction = model.predict(padded_sequence)
        intent_index = np.argmax(prediction)
        intent_name = label_encoder[intent_index]
        return intent_name
    except Exception as e:
        print(f"Error al predecir el intento: {e}")
        return None

def handle_message(message):
    try:
        intent_name = predict_intent(message)
        if intent_name is not None:
            response_text = get_response_by_intent(intent_name)
            if response_text:
                return response_text
        save_unclassified_message(message)
        return "No se ha detectado ningún intento"
    except Exception as e:
        print(f"Error al predecir intento: {e}")
        save_unclassified_message(message)
        return "Lo siento, no entiendo esto. Lo he guardado para aprenderlo más tarde."