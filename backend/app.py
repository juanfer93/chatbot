from flask import Flask, request, jsonify
from flask_cors import CORS
from services.training import train_model
from services.prediction import handle_message

app = Flask(__name__)
CORS(app)  

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get("message")
    response = handle_message(message)
    return jsonify({"response": response})

@app.route('/train', methods=['POST'])
def train():
    train_model()
    return jsonify({"message": "Modelo entrenado con éxito."})

if __name__ == '__main__':
    app.run(debug=True)
