import re
from typing import AsyncIterator, Optional

from langchain.schema import BaseMessage, HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel

from src.agent.vector_store_manager import VectorStoreManager


class BaseAgent:
    def __init__(
        self,
        model: BaseChatModel,
        vectorstore_manager: VectorStoreManager,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1024,
    ):
        self.model = model
        self.max_tokens = max_tokens
        self.vectorstore_manager = vectorstore_manager
        self.system_prompt = (
            system_prompt
            or """
Objetivo: Contestar las consultas del usuario basado unicamente el el siguiente contexto:
Contexto: {context}
Reglas: 
- Si el usuario saluda, responde con un saludo apropiado.
- No inventes respuestas, solo usa el contexto proporcionado para responder a la consulta del usuario.
- Si el contexto está vacio responde con "No hay información disponible sobre este tema.
- En caso de que la información necesaria no esté disponible en el contexto, responde con "No puedo esa pregunta con la información disponible.
"""
        )

    async def build_messages(self, prompt: str) -> list[BaseMessage]:
        vectorstore = await self.vectorstore_manager.load_vectorestore()
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        docs = await retriever.ainvoke(input=prompt)
        context_text = "\n\n".join([doc.page_content for doc in docs])

        if self.max_tokens < self.model.get_num_tokens(context_text):
            dict_tokens = [
                {"doc": doc, "tokens": self.model.get_num_tokens(doc.page_content)}
                for doc in docs
            ]
            dict_tokens = sorted(dict_tokens, key=lambda x: x["tokens"], reverse=True)
            docs = []
            tokens_sum = 0
            for doc_tokens in dict_tokens:
                if self.max_tokens < tokens_sum + doc_tokens["tokens"]:
                    break
                docs.append(doc_tokens["doc"])
                tokens_sum += doc_tokens["tokens"]

        messages = [
            SystemMessage(content=self.system_prompt.format(context=context_text)),
            HumanMessage(content=prompt),
        ]
        return messages

    async def query(self, prompt: str) -> str:
        messages = await self.build_messages(prompt)
        response = await self.model.ainvoke(messages)
        response_text = response.content
        if "<think>" in response_text and "</think>" in response_text:
            response_text = re.sub(
                r"<think>[\s\S]*?</think>",
                "",
                response_text,
            ).strip()

        return response_text

    async def query_stream(self, prompt: str) -> AsyncIterator[str]:
        messages = self.build_messages(prompt)
        async for token in self.model.astream(messages):
            yield token.content
