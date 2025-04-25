import argparse
import os
from modules.document_loader import DocumentProcessor
from modules.embedder import DocumentEmbedder
from modules.retriever import DocumentRetriever
from modules.generator import ResponseGenerator
import config

def setup_rag_system(rebuild_index=False):
    """Setup the RAG system"""
    document_processor = DocumentProcessor()
    embedder = DocumentEmbedder()

    # create or lod vector store
    if rebuild_index or not os.path.exists(config.VECTOR_DB_PATH):
        print("Building document index")
        chunks = document_processor.process_documents()
        vector_store = embedder.create_vector_store(chunks)
    else:
        print("Loading existing document index")
        vector_store = embedder.load_vector_store()

    # setup retriever and generator
    retriever = DocumentRetriever(vector_store).setup_retriever()
    generator = ResponseGenerator(retriever)

    return generator

def main:
    parser = argparse.ArgumentParser(description='RAG Application')
    parser.add_argument('--rebuild_index', action='store_true', help='Rebuild the document index')
    parser.add_argument('--query', type=str, help='Query to process')
    args = parser.parse_arges()

    generator =  setup_rag_system(rebuild_index=args.rebuild)

    if args.query:
        result = generator.generate_response(args.query)
        print("\nQuestion:", result["question"])
        print("\nResponse:", result["response"])
        print("\nSources:")
        for i, source in enumerate(result["sources"]):
            print(f"\nSource {i+1}:\n{source[:200]}...") # Print the first 200 characters of each source
    else: 
        # Interactive mode
        print("RAG System ready. Type 'exit' to quit.")
        while True:
            query = input("\nEnter your question: ")
            if query.lower() == 'exit':
                break
            result = generator.generate_response(query)
            print("\nQuestion:", result["answer"]) 
            print("\nSources:") 
            for i, source in enumerate(result["sources"]):
                print(f"\nSource {1+1}:\n{source[:200]}...") # Print the first 200 characters of each source

if __name__ == "__main__":
    main()                     
