from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
import os
import config

class DocumentRetriever:
    def __init__(self, vector_store: Chroma):
        os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
        self.vector_store = vector_store
        self.llm = ChatOpenAI(temperature=config.TEMPERATURE)

    def setup_retriever(self, use_compressor:True, top_k=4):
        """Setup the retriever with optional compression"""
        base_retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k":top_k}
        ) 

        if use_compression:
            compressor = LLMChainExtractor.from_llm(self.llm)
            retriever = ContextualCompressionRetriever(
                base_compressor=compressor,
                base_retriever=base_retriever,
            ) 
            return retriever

        return base_retriever       