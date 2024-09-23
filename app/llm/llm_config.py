
ai_textbook_model = "gemini-1.5-flash"

def get_ai_textbook_prompt(class_name, subject, topic):

    ai_textbook_prompt = [
        {"role": "user", "parts": f"You are the teacher. I'm {class_name}th class student. Can you help me with understanding the {topic} in the {subject} chapter? I will provide you the some text and explain it."},
        {"role": "model", "parts": "How can I help you?"},
    ]
    return ai_textbook_prompt