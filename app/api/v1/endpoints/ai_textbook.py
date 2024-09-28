from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.ai_textbook_dto import AIRequest, AIResponse
from app.models.models import User
from app.core.security import get_current_user
from app.db.mongodb import find_object, create_chat, create_object, get_chat
from app.llm.llm_config import get_ai_textbook_prompt
from app.db.redis import store_messages_in_redis, read_messages_from_redis
from app.llm.aitext_gemini import AITextbookGemini

router = APIRouter()
    
@router.post("/startChat", description="Start a new chat session")
async def start_chat(
    request: dict,
    current_user: User = Depends(get_current_user)
):
    user_id = current_user["id"]
    class_name = current_user["class_name"]
    subject = request["subject"]
    topic = request["topic"]
    book = request["book"]
    AITextbookChat = await find_object(collection_name="aitextbookchat", query={"user_id": user_id, "class_name": class_name, "subject": subject, "topic": topic, "book": book})
    if AITextbookChat is None:
        prompt = get_ai_textbook_prompt(class_name, subject, topic)
        chat_id = await create_chat(prompt)
        await create_object(collection_name="aitextbookchat", data={"user_id": user_id, "class_name": class_name, "subject": subject, "topic": topic, "book": book, "chat_id": chat_id})
        await store_messages_in_redis(chat_id, prompt)
        return {"message": "Chat started successfully", "chat_id": chat_id, "chat": prompt[1:]}

    else:
        chat_id = AITextbookChat["chat_id"]
        data = await get_chat(chat_id)
        await store_messages_in_redis(chat_id, data)
        return {"message": "Chat started successfully", "chat_id": chat_id, "chat": data[1:]}

@router.post("/sendMessage", description="Get the response from the AI model")
async def send_message(
    request: dict,
    current_user: User = Depends(get_current_user)
):
    chat_id = request["chat_id"]
    message = request["message"]
    flag = False
    retry = 5
    while retry:
        try:
            data = await read_messages_from_redis(chat_id)
            if data is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
            llm_ai = AITextbookGemini(next_key=flag)
            chat = llm_ai.prevChat(data)
            response = llm_ai.sendMessage(chat, message)
            data.append({"role": "user", "content": message})
            data.append({"role": "model", "content": response})
            await store_messages_in_redis(chat_id, data)
            return {"response": response}
        except Exception as e:
            retry -= 1
            print(f"Error: {e}")
            flag = True
        
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to get response from the AI model")


    


