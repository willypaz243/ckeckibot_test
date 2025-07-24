from typing import Optional

from langchain_openai.chat_models import ChatOpenAI

from src.agent.vector_store_manager import VectorStoreManager
from src.config import load_config

from . import BaseAgent


class OpenAIAgent(BaseAgent):
    def __init__(
        self,
        model_name: str,
        vectorstore_manager: VectorStoreManager,
        system_prompt: Optional[str] = None,
    ):
        config = load_config()
        super().__init__(
            ChatOpenAI(model=model_name, api_key=config.api_key),
            vectorstore_manager,
            system_prompt,
        )
