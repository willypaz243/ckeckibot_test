import json
import os

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_nebius import NebiusEmbeddings
from pydantic import SecretStr

from src.config import load_config

load_dotenv("../.env")


def load_json_files(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
                data.extend(json.load(f))
    return data


def create_vectorstore(data):
    # Initialize Nebius embeddings
    config = load_config()
    embeddings = NebiusEmbeddings(
        model="Qwen/Qwen3-Embedding-8B",
        api_key=SecretStr(config.api_key),
    )

    # Create FAISS vectorstore
    vectorstore = FAISS.from_texts(
        texts=[item["text"] for item in data], embedding=embeddings
    )

    # Save the vectorstore
    vectorstore.save_local("../vectorstore")

    return vectorstore


def main():
    # Create vectorstore directory if it doesn't exist
    os.makedirs("../vectorstore", exist_ok=True)

    # Load JSON data
    data = load_json_files("../base_docs")

    # Create and save vectorstore
    create_vectorstore(data)


if __name__ == "__main__":
    main()
