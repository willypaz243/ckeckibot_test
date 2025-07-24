from typing import Optional

from langchain_ollama.chat_models import ChatOllama

from src.agent.vector_store_manager import VectorStoreManager

from . import BaseAgent


class OllamaAgent(BaseAgent):
    def __init__(
        self,
        model_name: str,
        vectorstore_manager: VectorStoreManager,
        system_prompt: Optional[str] = None,
    ):
        super().__init__(
            ChatOllama(model=model_name),
            vectorstore_manager,
            system_prompt,
        )
