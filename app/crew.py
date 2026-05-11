from crewai import Crew, Process, Task
from agents import order_intake_agent, menu_agent, confirmation_agent

food_ordering_crew = Crew(
    agents=[order_intake_agent, menu_agent, confirmation_agent],
    process=Process.sequential,
    verbose=True,
    memory=False
)


def run_order_crew(user_message: str, conversation_context: str = "", current_order: str = ""):
    """Main function to run the full agentic flow"""
    
    from crewai import Task

    task1 = Task(
        description=f"""Previous Conversation:
{conversation_context}

Latest User Message: "{user_message}"

**Instructions:**
- Agar user confirmation de raha hai (yes, haan, confirm, place kar do, krdo etc.) toh 'CONFIRMED' return karo.
- Warna items + quantity parse karo.
- Agar user location bata raha hai (Delhi, Mumbai, etc.) toh usko note karo.""",
        expected_output="Parsed order details or 'CONFIRMED'",
        agent=order_intake_agent
    )

    task2 = Task(
        description="""User ke items ke hisaab se real restaurants search karo using Google Places API.
        Best matching restaurant suggest karo.
        Sirf ek best restaurant recommend karo, multiple mat dikhao.
        Location agar mention na ho toh 'Delhi' assume karo.""",
        expected_output="Best restaurant name, address, rating, items with approx price, total",
        agent=menu_agent
    )

    task3 = Task(
        description="""**Final Logic:**
- Agar 'CONFIRMED' mila hai toh yeh message do:
  "✅ Aapka order successfully placed ho gaya hai! 
   Restaurant: [Name]
   Total: ₹XXX 
   Order ID: ORD-XXXX"

- Warna clear summary dikhao aur pucho:
  "Kya aap is order ko confirm karna chahte hain? Ya koi change chahiye?"
""",
        expected_output="Clear summary with confirmation question or Order Placed message",
        agent=confirmation_agent
    )

    food_ordering_crew.tasks = [task1, task2, task3]
    
    print("🚀 Processing your order with real restaurants...\n")
    result = food_ordering_crew.kickoff()
    
    return result