import google.generativeai as genai
from app.llm.llm_config import get_ai_textbook_prompt, ai_textbook_model
from app.core.config import settings

index = 0

class AITextbookGemini:

    def __init__(self, next_key=False):
        self.api_keys = settings.gemini_api_keys
        global index
        if (next_key):
            index += 1
            index %= len(self.api_keys)
            self.ind = index
        else:
            self.ind = index

    def get_key():
        return self.api_keys[self.ind]
    
    def prevChat(self, prompt):
        genai.configure(api_key=self.get_key())
        model = genai.GenerativeModel(ai_textbook_model)
        chat = model.start_chat(
            history=prompt
        )
        return chat

    def sendMessage(self, chat, ques):
        response = chat.send_message(ques)
        return response.text
