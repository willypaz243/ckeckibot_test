from typing import Annotated

from fastapi import Depends

from src.agent.emb_models import load_nebius_embeddings
from src.agent.nebius_agent import NebiusAgent
from src.agent.vector_store_manager import VectorStoreManager
from src.config import Config, load_config


def get_emb_model(config: Annotated[Config, Depends(load_config)]):
    return load_nebius_embeddings("Qwen/Qwen3-Embedding-8B", config)


class VectorStoreManagerDep(VectorStoreManager):
    def __init__(
        self,
        emb_model: Annotated[VectorStoreManager, Depends(get_emb_model)],
    ):
        super().__init__(emb_model)


class NebiusAgentDep(NebiusAgent):
    def __init__(
        self,
        model_name: Annotated[str, Depends(lambda: "Qwen/Qwen3-235B-A22B")],
        vectorstore_manager: Annotated[
            VectorStoreManagerDep, Depends(VectorStoreManagerDep)
        ],
        system_prompt=None,
    ):
        super().__init__(
            model_name,
            vectorstore_manager,
            system_prompt,
        )
