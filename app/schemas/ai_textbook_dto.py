from pydantic import BaseModel

class AIRequest(BaseModel):
    study_class: str
    study_subject: str
    study_topic: str
    study_chat: str

class AIResponse(BaseModel):
    response: str