from database import fetch_training_data

def prepare_training_data():
    intents, examples = fetch_training_data()

    training_data = []
    for example in examples:
        intent_name = None
        for intent in intents:
            if example['intent_id'] == intent['id']:
                intent_name = intent['name']
                break
        if intent_name:
            response = intent.get("response", "No tengo una respuesta para eso.")
            training_data.append({
                "text": example['text'],  
                "intent": intent_name    
            })

    return training_data

if __name__ == "__main__":
    data = prepare_training_data()
    print(f"Datos preparados: {data[:5]}")  