# src/code_indexer.py

import os
import logging
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

logger = logging.getLogger(__name__)

def is_text_file(file_path):
    """Check if a file is a text file based on its extension."""
    text_extensions = {'.txt', '.md', '.js', '.py', '.java', '.c', '.cpp', '.h', '.cs', '.html', '.css', '.xml', '.json', '.yaml', '.yml', '.ini', '.cfg', '.conf'}
    return os.path.splitext(file_path)[1].lower() in text_extensions

def create_index(directory: str) -> Chroma:
    logger.info(f"Starting to index directory: {directory}")
    documents = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if is_text_file(file_path):
                try:
                    logger.debug(f"Attempting to load file: {file_path}")
                    loader = TextLoader(file_path, encoding='utf-8')
                    documents.extend(loader.load())
                    logger.debug(f"Successfully loaded file: {file_path}")
                except Exception as e:
                    logger.error(f"Error loading {file_path}: {e}")
    
    if not documents:
        logger.error(f"No valid text files found in the directory: {directory}")
        raise ValueError(f"No valid text files found in the directory: {directory}")
    
    logger.info(f"Loaded {len(documents)} documents")
    
    logger.info("Splitting texts")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    logger.info(f"Split into {len(texts)} text chunks")
    
    logger.info("Initializing embeddings")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    logger.info("Creating Chroma database")
    db = Chroma.from_documents(texts, embeddings, persist_directory="./chroma_db")
    logger.info("Finished creating index")
    return db