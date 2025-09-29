google_api_key = "AIzaSyBJXQkPMxPBD00uF4z9VOwRNEwxO4ahE40"
model="gemini-2.0-flash"

from google import genai
client = genai.Client(api_key=google_api_key)

contents="Give me a country I want to visit coming December with kids where is relaxing and safe"

prompt = f"""
You are an intent classifier. Given the user query below, reply with ONE intent category only, 
choosing from Travel, Weather, Food, Shopping, Math, Tech, Other.
User query: "{contents}"
"""

response = client.models.generate_content(
    model="gemini-2.0-flash", contents=prompt
)
print(response.text)