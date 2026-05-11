from crewai import Agent
from llm import get_crewai_llm
from menu_data import get_all_menus
from crewai import LLM
from dotenv import load_dotenv
import os
from tools import search_nearby_restaurants, get_restaurant_details

load_dotenv()

# === CrewAI Native LLM (Recommended for Gemini) ===
gemini_llm = LLM(
    model="gemini/gemini-2.5-flash-lite",     # or gemini/gemini-1.5-flash
    api_key=os.getenv("GEMINI_API_KEY"),     
    temperature=0.6,
    max_tokens=2048,
)

llm = get_crewai_llm()

# ==================== Agent 1: Order Intake Agent ====================
order_intake_agent = Agent(
    role = "Order Intake Specialist",
    goal = "User ki natural language order ko accurately samajhna aur parse karna",
    backstory = """Tu ek professional order taker hai jo Swiggy/Zomato pe kaam karta hai.
    User jo bhi bole usko item name, quantity aur special requests mein break karta hai.""",
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

# ==================== Agent 2: Menu & Restaurant Agent ====================
menu_agent = Agent(
    role="Menu & Restaurant Expert",
    goal="User ke items ko menu mein dhundna aur best possible match suggest karna. Agar exact match na mile to similar item suggest karo.",
    backstory="""Tu bahut helpful aur flexible hai. Agar user 'butter naan' maange aur 'Naan' ho to 'Naan' suggest kar. 
    Hamesha price aur restaurant ke saath clear information de.""",
    llm=gemini_llm,
    tools=[search_nearby_restaurants, get_restaurant_details],
    verbose=True,
    allow_delegation=False
)

# ==================== Agent 3: Confirmation Agent ====================
confirmation_agent = Agent(
    role="Order Confirmation Specialist",
    goal="Order summary dene ke baad user se final confirmation lena",
    backstory="""Tu polite aur clear hai. Order ka pura summary deta hai including total amount,
    aur user se confirm karwata hai ki order place karein ya nahi.""",
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

