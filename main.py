import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from graph import create_stable_scout_graph

load_dotenv()

def main():
    
    groq_key = os.getenv("GROQ_API_KEY")
    scout = create_stable_scout_graph(groq_key)
    
    user_input = "What is the yield for USDC? Is it better than 3.5%?"
    inputs = {"messages": [HumanMessage(content=user_input)]}
    
    print("StableScout is thinking...")
    for event in scout.stream(inputs, stream_mode="values"):
        event["messages"][-1].pretty_print()

if __name__ == "__main__":
    main()