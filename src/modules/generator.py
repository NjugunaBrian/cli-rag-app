from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.retrievers import BaseRetriever
import os
import config

class ResponseGenerator:
    def __init__(self, retriever: BaseRetriever):
        os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
        self.retriever = retriever
        self.llm = ChatOpenAI(model_name=config.LLM_MODEL, temperature=config.TEMPERATURE)

    def setup_qa_chain(self):
        """Setup the question-answering chain"""
        qa_chain = RetrievalQA.from_chain_type(
            llm = self.llm,
            chain_type = "stuff",
            retriever = self.retriever,
            return_source_documents = True,
        )
        return qa_chain

    def generate_response(self, query: str):
        """Generate a response to the query"""
        qa_chain = self.setup_qa_chain()
        result = qa_chain({"query": query})

        return {
            "question": query,
            "response": result["result"],
            "sources": [doc.page_content for doc in result["source_documents"]]
        }
                