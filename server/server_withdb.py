from flask import Flask, request, jsonify
from openai import OpenAI
from pymongo import MongoClient
import numpy as np
from sklearn.cluster import KMeans

# ==== Setup ====
app = Flask(__name__)
client = OpenAI()

# MongoDB connection (replace with your credentials)
mongo_client = MongoClient("mongodb+srv://<username>:<password>@cluster0.mongodb.net/")
db = mongo_client["intentDB"]
collection = db["queries"]

# ==== Helper functions ====
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def label_cluster(samples):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an intent classifier. Reply with one intent only, like Travel, Food, Weather, Shopping, Math, Tech, etc."},
            {"role": "user", "content": f"These are user queries: {samples}. What is the common intent?"}
        ]
    )
    return response.choices[0].message.content.strip()

def gpt_answer(query):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Answer user queries directly and concisely."},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content.strip()

# ==== Routes ====
@app.route("/classify", methods=["POST"])
def classify():
    data = request.json
    query = data.get("query")

    # 1. Compute embedding
    emb = get_embedding(query)

    # 2. Save query in MongoDB
    collection.insert_one({"query": query, "embedding": emb})

    # 3. Load all queries + embeddings
    docs = list(collection.find())
    queries = [doc["query"] for doc in docs]
    embeddings = [doc["embedding"] for doc in docs]

    # 4. Run clustering (k=5 → 5 general categories, tweakable)
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    labels = kmeans.fit_predict(embeddings)

    # 5. Find cluster of current query
    cluster_id = labels[-1]
    cluster_queries = [q for q, l in zip(queries, labels) if l == cluster_id]

    # 6. Get intent
    intent = label_cluster(cluster_queries)

    # 7. Get GPT answer (feedback is the response itself)
    feedback = gpt_answer(query)

    # 8. Save intent + feedback in MongoDB
    collection.update_one({"_id": docs[-1]["_id"]}, {"$set": {"intent": intent, "feedback": feedback}})

    return jsonify({
        "query": query,
        "intent": intent,
        "feedback": feedback
    })

# ==== Run ====
if __name__ == "__main__":
    app.run(port=5000, debug=True)
