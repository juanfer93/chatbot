import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from flask import Flask, request, jsonify
from flask_cors import CORS
from services.prediction import predict_intent, get_response_by_intent, save_unclassified_message
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        intent_name = predict_intent(user_message)
        if intent_name:
            response_text = get_response_by_intent(intent_name)
            if response_text:
                return jsonify({"response": response_text})
        
        save_unclassified_message(user_message)
        return jsonify({"response": "No se ha detectado ningún intento"})
    except Exception as e:
        print(f"Error: {e}")
        save_unclassified_message(user_message)
        return jsonify({"response": "Lo siento, no entiendo esto. Lo he guardado para aprenderlo más tarde."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)