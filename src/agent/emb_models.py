from src.config import Config


def load_openai_embeddings(model_name: str, config: Config):
    from langchain_openai.embeddings import OpenAIEmbeddings

    return OpenAIEmbeddings(model=model_name, api_key=config.api_key)


def load_nebius_embeddings(model_name: str, config: Config):
    from langchain_nebius.embeddings import NebiusEmbeddings

    return NebiusEmbeddings(model=model_name, api_key=config.api_key)


def load_ollama_embeddings(model_name: str):
    from langchain_ollama.embeddings import OllamaEmbeddings

    return OllamaEmbeddings(model=model_name)
