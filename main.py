from llm import get_crewai_llm
from crew import run_order_crew


# Global memory for conversation
conversation_context = ""
current_order_summary = ""

def main():

    global conversation_context, current_order_summary

    print("🤖 Food Ordering Agentic AI Started!")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("\n🍽️  Aap kya order karna chahte ho?: ").strip()

        if user_input.lower() in ['exit', 'quit', 'band karo']:
            print("👋 Thank you! Bye...")
            break

        if user_input.strip() == "":
            continue

        try:
            result = run_order_crew(user_message=user_input, conversation_context=conversation_context, current_order=current_order_summary)
            
            result_str = str(result)
            
            print("\n" + "="*60)
            print(result)
            print("="*60)
  
            conversation_context += f"\nUser: {user_input}\nAgent: {result}\n"
            

            if "successfully placed" in result.lower() or "✅" in result:
                print("\n🎉 Order Placed Successfully!")
                conversation_context = ""
                current_order_summary = ""
            else:
                if "Total Amount" in result or "Kul Rashi" in result:
                    current_order_summary = result

        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()