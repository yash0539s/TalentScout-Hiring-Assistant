import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API key -> stored in .env as: OPENAI_API_KEY=your_key_here
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def call_llm(prompt, user_input=None, candidate_data=None):
    """
    Calls OpenAI API (GPT model).
    Builds context-aware prompts for the chatbot.
    """
    text = prompt
    if user_input:
        text += f"\nUser: {user_input}\nAssistant:"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",   # safer to use the latest if you have access
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input or ""}
            ],
            max_tokens=300,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        return f" Error: {e}"

def save_candidate_data(data):
    """
    Saves candidate data locally in JSON lines format.
    """
    os.makedirs("data", exist_ok=True)
    with open("data/candidates.json", "a") as f:
        json.dump(data, f)
        f.write("\n")
