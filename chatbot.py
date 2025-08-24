import json
import os
import re
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
        self.current_field_index = 0  

        # Questions for each field
        self.field_reasons = {
            "Full Name": "Could you please share your full name? This will help us personalize the process.",
            "Email": "May I have your email address? We’ll use it for official communication regarding your application.",
            "Phone Number": "Could you provide your phone number? In case of interviews, our team may contact you directly.",
            "Years of Experience": "How many years of professional experience do you have? This helps us understand your expertise level.",
            "Desired Position": "Which position are you most interested in applying for? This ensures we align you with the right role.",
            "Current Location": "Where are you currently located? This helps us consider time zones and location preferences.",
            "Tech Stack": "What are the primary tools, languages, or frameworks you are comfortable working with?"
        }

        # Acknowledgments for each valid answer
        self.field_acknowledgments = {
            "Full Name": "Thank you, {value}. I’ll use your name for personalization.",
            "Email": "Thanks, we’ll use {value} for official communication.",
            "Phone Number": "Got it. {value} may be used to contact you directly if needed.",
            "Years of Experience": "Noted, {value} years of experience. That gives us a good idea of your expertise.",
            "Desired Position": "Great, we’ll align your application with the {value} role.",
            "Current Location": "Thank you. Being in {value} helps us consider time zones or relocation options.",
            "Tech Stack": "Excellent, your skills in {value} will help us prepare relevant technical questions."
        }

    def validate_field(self, field, value):
        """Validate and correct candidate input in a professional tone"""
        if field == "Email":
            if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                return False, "That email address doesn’t seem valid. Could you please provide a correct one?"
        elif field == "Phone Number":
            if not re.match(r"^\+?\d{7,15}$", value):
                return False, "That phone number doesn’t look correct. Please provide a valid number with country code if applicable."
        elif field == "Years of Experience":
            if not value.isdigit() or int(value) < 0 or int(value) > 50:
                return False, "Could you specify a valid number of years of experience (0–50)?"
        elif field == "Full Name":
            if len(value.split()) < 2:
                return False, "Please provide your full name including both first and last name."
        elif field == "Tech Stack":
            if not value or len(value) < 2:
                return False, "Could you list a few tools, frameworks, or languages that you primarily work with?"

        return True, value.strip()

    def chat(self, user_input):
        # Exit condition
        if user_input.lower() in ["quit", "exit", "bye"]:
            save_candidate_data(self.candidate_data)
            return "Thank you for your time. We appreciate your interest and will be in touch with next steps."

        # Stage 1: Collect candidate info
        if self.stage == "info":
            if not self.candidate_data and user_input.lower() in ["hi", "hello", "hey"]:
                first_field = self.required_fields[self.current_field_index]
                return f"Hello, I’m here to assist with your application. {self.field_reasons[first_field]}"

            if self.current_field_index < len(self.required_fields):
                current_field = self.required_fields[self.current_field_index]

                # Validate input
                valid, feedback = self.validate_field(current_field, user_input.strip())
                if not valid:
                    return feedback  

                # Save valid input
                self.candidate_data[current_field] = feedback
                ack_msg = self.field_acknowledgments[current_field].format(value=feedback)
                self.current_field_index += 1  

                # Next step
                if self.current_field_index < len(self.required_fields):
                    next_field = self.required_fields[self.current_field_index]
                    return f"{ack_msg}\n\n{self.field_reasons[next_field]}"

                # All fields collected
                self.stage = "questions"
                summary = "\n".join([f"{k}: {v}" for k, v in self.candidate_data.items()])
                return f"{ack_msg}\n\nThank you for providing your details. Here is a quick summary:\n\n{summary}\n\nShall we proceed with a few technical questions?"

        # Stage 2: Technical questions
        elif self.stage == "questions":
            tech_stack = self.candidate_data.get("Tech Stack", "").strip()
            tech_list = [tech.strip() for tech in tech_stack.split(",") if tech.strip()]
            all_questions = ""

            for tech in tech_list:
                q_prompt = TECH_QUESTION_PROMPT.format(tech_stack=tech)
                q_response, _ = call_llm(q_prompt, "", self.candidate_data)
                all_questions += f"\n{tech}:\n{q_response}\n"

            self.stage = "done"
            save_candidate_data(self.candidate_data)
            return f"Here are some technical questions tailored to your skills:\n{all_questions}\nWe wish you the best in preparing for the next stage."

        # Stage 3: Done
        else:
            if user_input.lower() in ["review", "again"]:
                self.stage = "questions"
                return "Certainly, let’s go over your technical questions once again."
            return "Your details have been recorded. If you are ready, you may type 'quit' to exit."