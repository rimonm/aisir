# src/code_chat.py

import logging
from langchain.chat_models import ChatAnthropic
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

class CodeChat:
    def __init__(self, db_path: str):
        logger.info(f"Initializing CodeChat with database path: {db_path}")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.db = Chroma(persist_directory=db_path, embedding_function=embeddings)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.qa = ConversationalRetrievalChain.from_llm(
            ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0),
            self.db.as_retriever(),
            memory=self.memory
        )
        logger.info("CodeChat initialized successfully")

    def chat(self, query: str) -> str:
        logger.info(f"Received chat query: {query}")
        try:
            response = self.qa({"question": query})
            logger.info("Successfully generated response")
            return response['answer']
        except Exception as e:
            logger.error(f"Error generating chat response: {e}")
            raise

    def generate_component(self, description: str) -> str:
        logger.info(f"Received component generation request: {description}")
        prompt = f"""Based on the existing code in the repository, generate a new component that matches this description: {description}
        
        Follow best practices for the appropriate programming language and include brief comments explaining the component's purpose.
        
        Generate the complete component code:
        """
        try:
            response = self.chat(prompt)
            logger.info("Successfully generated component")
            return response
        except Exception as e:
            logger.error(f"Error generating component: {e}")
            raise