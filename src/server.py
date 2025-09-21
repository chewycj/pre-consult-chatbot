# Not in use, kept for reference
from flask import Flask, request, jsonify
from src.chat_engine import get_engine

app = Flask(__name__)
engine = get_engine()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    result = engine.process_message(user_input)
    return jsonify({"response": result.get("response", "[No response]")})

if __name__ == "__main__":
    app.run(port=8000)