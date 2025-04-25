from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text-splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
import os
import config

Class DocumentProcessor:
    def _init__(self, data_dir=config.DATA_PATH):
        self.data_dir = data_dir
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )

    def load_documents(self) -> List[Document]:
        """Load documents from the data directory"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            raise FileNotFoundError(f"No documents found in {self.data_dir}")

        loader = DirectoryLoader(self.data_dir, glob="**/*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load();
        return documents

    def process_documents(self) -> List[Document]:
        """Load and split documents into chunks"""
        documents = self.load_documents()
        chunks = self.text_splitter.split_documents(documents)
        print(f"Split {len(documents)} documents into {len(chunks)} chunks")
        return chunks         