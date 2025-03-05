from database import fetch_training_data

def prepare_training_data():
    intents, examples = fetch_training_data()

    intent_map = {intent['id']: intent['name'] for intent in intents}
    training_data = [
        {"text": example['text'], "intent": intent_map[example['intent_id']]}
        for example in examples if example['intent_id'] in intent_map
    ]

    return training_data

if __name__ == "__main__":
    data = prepare_training_data()
    print(f"Datos preparados: {data[:5]}")  