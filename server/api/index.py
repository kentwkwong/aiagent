from flask import Flask, request, jsonify
from service.ai_service import ask_ai
from service.db_service import get_user_history


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "heeeeeeello world"})


@app.route("/ai/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        email = data.get("email")
        question = data.get("question")

        if not email or not question:
            return jsonify({"error": "email and question are required"}), 400

        result = ask_ai(email, question)
        return jsonify(result)

    except Exception as e:
        # Log error if needed
        print(f"Error in /ai/ask: {e}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@app.route("/ai/history", methods=["GET"])
def history():
    try:
        email = request.args.get("email")
        if not email:
            return jsonify({"error": "email is required"}), 400

        history = get_user_history(email)
        return jsonify({"email": email, "history": history})

    except Exception as e:
        print(f"Error in /ai/history: {e}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
