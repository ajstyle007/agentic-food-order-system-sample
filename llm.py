import os
from dotenv import load_dotenv
import google.genai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()

def get_crewai_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0.7,
        google_api_key=os.getenv("GEMINI_API_KEY"),
        max_tokens=2048,
        convert_system_message_to_human=True
    )