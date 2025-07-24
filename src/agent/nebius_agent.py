from typing import Optional

from langchain_openai import ChatOpenAI

from src.agent.vector_store_manager import VectorStoreManager
from src.config import load_config

from . import BaseAgent


class NebiusAgent(BaseAgent):
    def __init__(
        self,
        model_name: str,
        vectorstore_manager: VectorStoreManager,
        system_prompt: Optional[str],
    ) -> None:
        config = load_config()
        super().__init__(
            ChatOpenAI(
                base_url="https://api.studio.nebius.com/v1/",
                model=model_name,
                api_key=config.api_key,
            ),
            vectorstore_manager,
            system_prompt,
            max_tokens=40960,
        )
        self.system_prompt = "Do not think\n" + self.system_prompt
