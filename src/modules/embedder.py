from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from typing import List
from langchain.schema import Document
import os
import config

class DocumentEmbedder:
    def __init__(self, persist_directory=config.VECTOR_DB_PATH):
        os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
        self.embeddings = OpenAIEmbeddings()
        self.persist_directory = persist_directory

    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """Create and persist a vector store from documents"""
        if not os.path.exists(os.path.dirname(self.persist_directory)):
            os.makedirs(os.path.dirname(self.persist_directory))

        vector_store = Chroma.from_documents(
            documents=documents,
            embedding = self.embeddings,
            persist_directory=self.persist_directory
        )

        vector_store.persist()
        return vector_store

    def load_vector_store(self) -> Chroma:
        """Load an existing vector store"""
        if not os.path.exists(self.persist_directory):
            raise FileNotFoundError(f"No vector store found at {self.persist_directory}")

        vector_store = Chroma(
            persist_directory = self.persist_directory,
            embedding_function=self.embeddings
        )   
        return vector_store             
