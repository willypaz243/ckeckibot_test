from pydantic import BaseModel


class ChatMessage(BaseModel):
    content: str
