import json
import os
from prompts import COLLECT_INFO_PROMPT, TECH_QUESTION_PROMPT
from utils import call_llm, save_candidate_data

class HiringAssistant:
    def __init__(self):
        self.conversation = []
        self.candidate_data = {}
        self.stage = "info"

    def chat(self, user_input):
        # Exit case
        if user_input.lower() in ["quit", "exit", "bye"]:
            save_candidate_data(self.candidate_data)
            return "Thanks for your time! We’ll be in touch with next steps."

        if self.stage == "info":
            response = call_llm(COLLECT_INFO_PROMPT, user_input, self.candidate_data)
            if "tech stack" in response.lower():
                self.stage = "questions"
            return response

        elif self.stage == "questions":
            tech_stack = self.candidate_data.get("Tech Stack", "")
            questions = call_llm(TECH_QUESTION_PROMPT.format(tech_stack=tech_stack))
            self.stage = "done"
            save_candidate_data(self.candidate_data)
            return f"Here are your technical questions:\n\n{questions}"

        else:
            return "Conversation completed. Type 'quit' to exit."

