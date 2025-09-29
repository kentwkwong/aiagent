google_api_key = "AIzaSyBJXQkPMxPBD00uF4z9VOwRNEwxO4ahE40"
model="gemini-2.0-flash"

# response = client.models.generate_content(
#     model="gemini-2.0-flash", contents="Give me a country I want to visit coming December with kids where is relaxing and safe"
# )
# print(response.text)


from flask import Flask, request, jsonify
from google import genai

client = genai.Client(api_key=google_api_key)

app = Flask(__name__)

# ==== In-memory storage ====
intent_history = {}  # { intent: [ {query, answer} ] }

# ==== Helper functions ====

def get_gpt_answer(user_query):
    """
    Use Gemini to generate a response to the user's query.
    """
    response = client.models.generate_content(
        model=model,
        contents=user_query
    )
    return response.text

def classify_intent(user_query):
    """
    Ask Gemini to classify the intent of a query.
    Returns a single intent like Travel, Weather, Food, Shopping, Math, Tech, etc.
    """
    prompt = f"""
    You are an intent classifier. Given the user query below, reply with ONE intent category only, 
    choosing from Travel, Weather, Food, Shopping, Math, Tech, Other.
    User query: "{user_query}"
    """
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    # Strip extra whitespace/newlines
    return response.text.strip()

# ==== Flask Routes ====

@app.route("/query", methods=["POST"])
def handle_query():
    data = request.json
    user_query = data.get("query")
    if not user_query:
        return jsonify({"error": "Query is required"}), 400

    # 1️⃣ Classify intent
    intent = classify_intent(user_query)

    # 2️⃣ Get GPT answer
    answer = get_gpt_answer(user_query)

    # 3️⃣ Save to history
    if intent not in intent_history:
        intent_history[intent] = []
    intent_history[intent].append({"query": user_query, "answer": answer})

    # 4️⃣ Respond
    return jsonify({
        "query": user_query,
        "intent": intent,
        "answer": answer
    })


@app.route("/history", methods=["GET"])
def get_history():
    """
    Return the full history grouped by intent
    """
    return jsonify(intent_history)


@app.route("/history/<intent_name>", methods=["GET"])
def get_history_by_intent(intent_name):
    """
    Return history only for a specific intent
    """
    return jsonify(intent_history.get(intent_name, []))


# ==== Run Flask ====
if __name__ == "__main__":
    app.run(port=5000, debug=True)
