# TalentScout - AI Hiring Assistant 🤖

## Project Overview

TalentScout is an AI-powered Hiring Assistant designed for initial candidate screening. It helps recruitment teams gather essential candidate information and generate technical questions based on the candidate’s declared tech stack.

Key features:

* Step-by-step collection of candidate details
* Context-aware conversation flow
* Tech-stack-specific technical question generation
* Secure storage of candidate data
* Interactive Streamlit chat interface

---

## Features

1. **User Interaction**

   * Greets candidates and explains purpose
   * Collects: Full Name, Email, Phone Number, Experience, Desired Position, Location, Tech Stack
   * Moves seamlessly to technical question generation

2. **Technical Question Generation**

   * Generates 3–5 technical questions per technology in candidate’s tech stack
   * Handles multiple technologies: e.g., Python, Django, React

3. **Data Handling**

   * Stores candidate information locally in `data/candidates.json`
   * Email and phone number are hashed for privacy

4. **UI/UX**

   * Streamlit-based chat interface

---

## Installation Instructions

1. Clone the repository:

```bash
git clone <repository_url>
cd TalentScout
```

2. Create a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set OpenAI API key in `.env` file:

```
OPENAI_API_KEY=your_openai_api_key
```

---

## Usage

1. Launch the Streamlit app:

```bash
streamlit run app.py
```

2. Interact with the chatbot in the browser:

   * Provide your details step by step
   * Enter your tech stack
   * Receive technical questions



---

## Technical Details

* **Programming Language:** Python 3.x
* **Libraries Used:** Streamlit, OpenAI, python-dotenv
* **LLM Model:** GPT-4o-mini (for candidate info extraction & question generation)
* **Architecture:** Modular (`chatbot.py`, `utils.py`, `prompts.py`, `app.py`)
* **Data Storage:** JSON files in `data/` folder

---

## Prompt Design

1. **Candidate Info Prompt:** Guides LLM to collect essential info step-by-step, politely, and concisely.
2. **Technical Question Prompt:** Generates 3–5 challenging but fair questions per technology in the declared tech stack.

---

## Challenges & Solutions

* **Maintaining conversation context:** Solved by using `self.stage` in `HiringAssistant`.
* **Handling multi-tech stack:** Split input by commas and looped through each tech for question generation.
* **Data privacy:** Hashing emails and phone numbers before saving.

---

## Future Improvements (Optional)

* Deploy to cloud (AWS, GCP) for live demo
* Evaluate candidate responses automatically
* Add scoring/ranking system based on answers

---

## Contact

For any questions regarding the project, contact **\[Yash malviya / yashmalviya9890@gmail.com]**.
