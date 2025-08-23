import json
import os
import requests

# Hugging Face API token -> get from https://huggingface.co/settings/tokens
HF_API_KEY = os.getenv("HF_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def call_llm(prompt, user_input=None, candidate_data=None):
    """
    Calls Hugging Face Inference API with Mistral-7B-Instruct.
    Builds context-aware prompts for the chatbot.
    """
    text = prompt
    if user_input:
        text += f"\nUser: {user_input}\nAssistant:"

    response = requests.post(API_URL, headers=headers, json={"inputs": text})

    try:
        output = response.json()
        # Hugging Face returns [{"generated_text": "..."}]
        if isinstance(output, list) and "generated_text" in output[0]:
            return output[0]["generated_text"].split("Assistant:")[-1].strip()
        else:
            return f" Unexpected response: {output}"
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
