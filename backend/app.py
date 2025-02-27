from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

from services.prediction import handle_message

app = Flask(__name__)
CORS(app)  

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        response = handle_message(user_message)
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error: {e}")  
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)