# utils.py1
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
import hashlib

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def call_llm(prompt, user_input=None, candidate_data=None):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input or ""}
        ],
        max_tokens=300,
        temperature=0.7
    )

    response_text = response.choices[0].message.content.strip()

    # Extract fields safely
    extracted_data = {}
    fields_to_extract = [
        "Full Name", "Email", "Phone Number",
        "Years of Experience", "Desired Position",
        "Current Location", "Tech Stack"
    ]

    candidate_keys_norm = []
    if candidate_data:
        candidate_keys_norm = [k.lower().replace(" ", "") for k in candidate_data.keys()]

    for line in response_text.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            key_norm = key.lower().replace(" ", "")
            for field in fields_to_extract:
                field_norm = field.lower().replace(" ", "")
                if key_norm == field_norm and field_norm not in candidate_keys_norm:
                    extracted_data[field] = value

    return response_text, extracted_data


def save_candidate_data(data):
    os.makedirs("data", exist_ok=True)

    # Anonymize sensitive fields
    if "Email" in data:
        data["Email"] = hashlib.sha256(data["Email"].encode()).hexdigest()
    if "Phone Number" in data:
        data["Phone Number"] = hashlib.sha256(data["Phone Number"].encode()).hexdigest()

    with open("data/candidates.json", "a") as f:
        json.dump(data, f)
        f.write("\n")
