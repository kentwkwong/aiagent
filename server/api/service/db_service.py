import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

db_conn = os.getenv('DB_CONNECTION_STRING')
client = MongoClient(db_conn)
db = client["aiagent"]
answer_collection = db["answers"]


def save_message(email, intent, question, answer):
    try:
        timestamp = datetime.utcnow()

        # Push the message into the correct intent array
        answer_collection.update_one(
            {"email": email, "conversations.intent": intent},
            {"$push": {"conversations.$.messages": {
                "question": question,
                "answer": answer,
                "timestamp": timestamp
            }}},
            upsert=False
        )

        # If intent does not exist yet, create it
        answer_collection.update_one(
            {"email": email, "conversations.intent": {"$ne": intent}},
            {"$push": {"conversations": {
                "intent": intent,
                "messages": [
                    {"question": question, "answer": answer, "timestamp": timestamp}
                ]
            }}},
            upsert=True
        )
    except Exception as e:
        print(f"Error save_message {email}: {e}")
        raise e

def get_user_history(email):
    try:

        user = answer_collection.find_one({"email": email})
        if not user:
            return []

        messages = []
        for conv in user.get("conversations", []):
            for msg in conv.get("messages", []):
                messages.append({
                    "intent": conv.get("intent"),
                    "question": msg.get("question"),
                    "answer": msg.get("answer"),
                    "timestamp": msg.get("timestamp")
                })
        return messages
    
    except Exception as e:
        print(f"Error get_user_history {email}: {e}")
        raise e