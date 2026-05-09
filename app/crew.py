from crewai import Crew, Process, Task
from agents import order_intake_agent, menu_agent, confirmation_agent
import os 

#lets create crew
food_ordering_crew = Crew(
    agents=[order_intake_agent, menu_agent, confirmation_agent],
    process=Process.sequential, #first intake -> then menu -> then confirmation
    verbose=True,
    memory=False,
    embedder=None
)


def run_order_crew(user_message: str, conversation_context: str = "", current_order: str = ""):
    """This is main fucntion who will run full flow"""

    # Task 1: Order Intake
    task1 = Task(
        description=f"""Previous Conversation Context:
        {conversation_context}

        Current Active Order (if any):
        {current_order}

        Latest User Message: "{user_message}"

        **Important Instructions:**
        - Agar user confirmation de raha hai (yes, haan, confirm, place kar do, order kar do etc.) aur pehle se koi order summary hai, toh 'CONFIRMED' return karo.
        - Warna normal order parse karo (items + quantity).""",
        expected_output="Either 'CONFIRMED' or parsed order details",
        agent=order_intake_agent
    )

    # Task 2: Menu & Restaurant Search
    task2 = Task(
        description="""Agar user ne naya order diya hai toh menu search karo aur summary banao.
        Agar 'CONFIRMED' hai toh is task ko skip karne ki koshish karo.""",
        expected_output="Restaurant, items with price, total amount",
        agent=menu_agent
    )

    # Task 3: Final Confirmation
    task3 = Task(
        description="""Agar intake agent ne 'CONFIRMED' bola hai toh final message mein bol do:
        "✅ Aapka order successfully placed ho gaya hai!"

        Warana normal summary dikhao aur confirmation maango.""",
        expected_output="Final response to user",
        agent=confirmation_agent
    )

    # assign tasks to crew
    food_ordering_crew.tasks = [task1, task2, task3]

    print("🚀 Order Processing start...\n")
    result = food_ordering_crew.kickoff()

    return result