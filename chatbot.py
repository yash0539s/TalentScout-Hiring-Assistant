import json
import os
from prompts import COLLECT_INFO_PROMPT, TECH_QUESTION_PROMPT
from utils import call_llm, save_candidate_data

class HiringAssistant:
    def __init__(self):
        self.candidate_data = {}
        self.stage = "info"
        self.required_fields = [
            "Full Name",
            "Email",
            "Phone Number",
            "Years of Experience",
            "Desired Position",
            "Current Location",
            "Tech Stack"
        ]

    def chat(self, user_input):
        # ------------------ Exit Case ------------------
        if user_input.lower() in ["quit", "exit", "bye"]:
            save_candidate_data(self.candidate_data)
            return "Thanks for your time! We’ll be in touch with next steps."

        # ------------------ Info Collection Stage ------------------
        if self.stage == "info":
            missing_fields = [f for f in self.required_fields if not self.candidate_data.get(f)]

            # First greeting handling
            if not self.candidate_data and user_input.lower() in ["hi", "hii", "hello", "hey"]:
                return f"Hello! Let's get started. Please provide your {missing_fields[0]}."

            if not missing_fields:
                self.stage = "questions"
                return "Great! I have all your details. Let's move to technical questions."

            # Ask about the first missing field
            current_field = missing_fields[0]
            prompt_with_missing = COLLECT_INFO_PROMPT + f"\nPlease ask about: {current_field}"

            # Call LLM to process input
            response, extracted_data = call_llm(prompt_with_missing, user_input, self.candidate_data)

            # Update candidate data
            if extracted_data.get(current_field):
                self.candidate_data[current_field] = extracted_data[current_field]
            else:
                if user_input.lower() not in ["hi", "hii", "hello", "hey"]:
                    self.candidate_data[current_field] = user_input.strip()

            # Check if all fields are filled
            missing_fields = [f for f in self.required_fields if not self.candidate_data.get(f)]
            if not missing_fields:
                self.stage = "questions"
                return "Great! I have all your details. Let's move to technical questions."

            return f"Thanks! Now, please provide your {missing_fields[0]}."

        # ------------------ Technical Questions Stage ------------------
        elif self.stage == "questions":
            tech_stack = self.candidate_data.get("Tech Stack", "").strip()
            tech_list = [tech.strip() for tech in tech_stack.split(",")]
            all_questions = ""

            for tech in tech_list:
                q_prompt = TECH_QUESTION_PROMPT.format(tech_stack=tech)
                q_response, _ = call_llm(q_prompt, "", self.candidate_data)
                all_questions += f"\n{tech} Questions:\n{q_response}\n"

            self.stage = "done"
            save_candidate_data(self.candidate_data)
            return f"Here are your technical questions:{all_questions}"


        # ------------------ Done Stage ------------------
        else:
            if user_input.lower() in ["review", "again"]:
                self.stage = "questions"
                return "Sure! Let's go over the technical questions again."
            return "Conversation completed. Type 'quit' to exit."

