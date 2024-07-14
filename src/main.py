# src/main.py

import streamlit as st
import logging
import os
from dotenv import load_dotenv
from code_indexer import create_index
from code_chat import CodeChat
from logging_config import setup_logging

load_dotenv()
setup_logging()
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting the application")
    st.title("Code Repository Chat")

    if 'chat' not in st.session_state:
        repo_path = st.text_input("Enter the path to your code repository:")
        if repo_path and os.path.isdir(repo_path):
            try:
                logger.info(f"Attempting to index repository: {repo_path}")
                with st.spinner("Indexing repository..."):
                    create_index(repo_path)
                st.session_state.chat = CodeChat("./chroma_db")
                st.success("Repository indexed successfully!")
                logger.info("Repository indexed successfully")
            except ValueError as e:
                error_message = f"Error: {str(e)}"
                logger.error(error_message)
                st.error(error_message)
        elif repo_path:
            error_message = "Invalid directory path. Please enter a valid path."
            logger.error(error_message)
            st.error(error_message)

    if 'chat' in st.session_state:
        query = st.text_input("Ask a question or describe a component to generate:")
        if query:
            logger.info(f"Received query: {query}")
            with st.spinner("Generating response..."):
                try:
                    if "generate" in query.lower() and "component" in query.lower():
                        logger.info("Generating component")
                        response = st.session_state.chat.generate_component(query)
                        st.code(response)
                    else:
                        logger.info("Generating chat response")
                        response = st.session_state.chat.chat(query)
                        st.write(response)
                    logger.info("Response generated successfully")
                except Exception as e:
                    error_message = f"An error occurred: {str(e)}"
                    logger.error(error_message)
                    st.error(error_message)

if __name__ == "__main__":
    main()