import os
from dotenv import load_dotenv
# import google.generativeai as genai
import google.genai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# def get_llm_response(prompt: str) -> str:
    
#     model = genai.GenerativeModel("gemini-2.5-flash-lite")
    
#     try:
#         response = model.generate_content(prompt)
#         clean_text = response.text.replace("```json", "").replace("```", "").strip()
#         return clean_text
#     except Exception as e:
#         return f"Error: {e}"

def get_crewai_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0.7,
        google_api_key=os.getenv("GEMINI_API_KEY"),
        max_tokens=2048,
        convert_system_message_to_human=True
    )



genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_llm_response(prompt: str) -> str:
    """Simple raw Gemini call"""
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        return clean_text
    except Exception as e:
        return f"Error: {str(e)}"
    

# Test function
if __name__ == "__main__":
    print("Testing LLM...")
    print(get_llm_response("Hello bhai, ek chhota test response de"))

    llm = get_crewai_llm()
    response = llm.invoke([HumanMessage(content="Kaise ho?")])
    print("\nLangChain Response:", response.content)

