import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from graph import create_stable_scout_graph

# 1. Load environment variables from your .env file
load_dotenv()

def main():
    # 2. Configuration & Key Verification
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("CRITICAL ERROR: GROQ_API_KEY not found. Please check your .env file.")
        return

    # 3. Initialize the Multi-Agent Brain
    # This calls the graph you defined in graph.py
    print("Initializing StableScout Multi-Agent Intelligence...")
    scout = create_stable_scout_graph(api_key)
    
    # 4. Define the prompt
    # Now that we have a Risk Agent, we can ask more complex questions
    user_query = "What is the USDC yield on Aave? If it's above 3%, is it safe for a large deposit?"
    inputs = {"messages": [HumanMessage(content=user_query)]}
    
    print(f"User Request: {user_query}")
    print("-" * 50)

    # 5. Execute the Graph and Stream the State
    # stream_mode="values" allows us to see the full message chain as it grows
    try:
        for event in scout.stream(inputs, stream_mode="values"):
            if "messages" in event:
                # Retrieve and print only the latest message added to the conversation
                latest_message = event["messages"][-1]
                latest_message.pretty_print()
                print("-" * 30)
    except Exception as e:
        print(f"An error occurred during graph execution: {e}")

if __name__ == "__main__":
    main()