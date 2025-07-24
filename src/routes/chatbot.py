from fastapi import APIRouter, Depends, WebSocket

from src.routes.deps import NebiusAgentDep
from src.routes.schemas import ChatMessage

chatbot_router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@chatbot_router.post("/chat")
async def chat(query: ChatMessage, agent: NebiusAgentDep = Depends()) -> ChatMessage:
    response = await agent.query(query.content)
    return ChatMessage(content=response)


@chatbot_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, agent: NebiusAgentDep = Depends()):
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        async for token in agent.query_stream(data):
            await websocket.send_text(token)
        await websocket.close()
    except Exception:
        await websocket.close(code=1001)
