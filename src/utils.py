# src/utils.py
import os
from dotenv import load_dotenv

def load_api_key():
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in .env file")
    return api_key