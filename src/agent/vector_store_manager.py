import json
import os

import aiofiles
from langchain_community.document_loaders import CSVLoader, JSONLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


class VectorStoreManager:
    def __init__(self, emb_model: Embeddings) -> None:
        self.emb_model = emb_model
        self.docs_path = "base_docs"
        self.vectorstore_path = "vectorstore"

    async def load_vectorestore(self) -> FAISS:
        if os.path.exists(self.vectorstore_path):
            return FAISS.load_local(
                self.vectorstore_path,
                self.emb_model,
                allow_dangerous_deserialization=True,
            )

        vectorstore = await FAISS.afrom_documents(
            [Document(page_content="")],
            self.emb_model,
        )
        await vectorstore.adelete(list(vectorstore.index_to_docstore_id.values()))
        vectorstore.save_local(self.vectorstore_path)
        return vectorstore

    async def load_ids_dict(self):
        if os.path.exists(f"{self.docs_path}/ids.json"):
            async with aiofiles.open(f"{self.docs_path}/ids.json", "r") as f:
                data = await f.read()
                return json.loads(data)
        else:
            ids_dict = {}
        return ids_dict

    async def save_ids_dict(self, ids_dict: dict):
        async with aiofiles.open(f"{self.docs_path}/ids.json", "w") as f:
            await f.write(json.dumps(ids_dict))

    async def add_document(self, file_name: str, document: bytes) -> list[str]:
        file_path = f"{self.docs_path}/{file_name}"
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(document)

        loader = None
        if file_name.endswith(".csv"):
            loader = CSVLoader(file_path)
        elif file_name.endswith(".json"):
            loader = JSONLoader(file_path, ".", text_content=False)

        docs = await loader.aload() if loader else None
        if not docs:
            raise ValueError("No documents found in the file.")

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = splitter.split_documents(docs)
        vectorstore = await self.load_vectorestore()
        ids = await vectorstore.aadd_documents(docs)

        vectorstore.save_local(self.vectorstore_path)

        ids_dict = await self.load_ids_dict()

        ids_dict[file_name] = ids

        await self.save_ids_dict(ids_dict)

        return ids

    def list_documents(self):
        return [f for f in os.listdir(self.docs_path) if "ids" not in f]

    async def delete_document(self, file_name: str) -> bool:
        ids_dict = await self.load_ids_dict()
        file_path = f"{self.docs_path}/{file_name}"
        if os.path.exists(file_path):
            os.remove(file_path)
        vectorstore = await self.load_vectorestore()
        ids = ids_dict.get(file_name, [])
        if not ids:
            return False
        try:
            return bool(await vectorstore.adelete(ids))
        except Exception as _:
            return False
