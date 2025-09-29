from google import genai
from .db_service import save_message
from dotenv import load_dotenv
import os

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=google_api_key)

def ask_ai(email, question):
    try:
        model = "gemini-2.0-flash"
        prompt = f"""
        You are an intent classifier. Given the user query below, reply with ONE intent category only, 
        choosing from Travel, Weather, Food, Shopping, Math, Tech, Other.
        User query: "{question}"
        """
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        intent = response.text.strip()
        response = client.models.generate_content(
            model=model,
            contents=question
        )
        answer = response.text.strip()
        # 3️⃣ Save to MongoDB Atlas
        save_message(email, intent, question, answer)
        return {"intent": intent, "answer": answer}
    except Exception as e:
        print(f"Error ask_ai: {e}")
        return {"error": "Internal server error", "details": str(e)}

