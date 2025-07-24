from fastapi import APIRouter

from .chatbot import chatbot_router
from .documents import docs_router

api_router = APIRouter(prefix="/api")
api_router.include_router(chatbot_router)
api_router.include_router(docs_router)
