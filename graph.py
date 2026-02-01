import operator
from typing import Annotated, TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from tools import get_stablecoin_yield  # Importing our SE logic

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

def create_stable_scout_graph(api_key: str):
    # Bind the blockchain tool to the LLM
    tools = [get_stablecoin_yield]
    llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=api_key).bind_tools(tools)

    def call_model(state: AgentState):
        response = llm.invoke(state["messages"])
        return {"messages": [response]}

    def should_continue(state: AgentState):
        if state["messages"][-1].tool_calls:
            return "tools"
        return END

    # Define Graph
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue, ["tools", END])
    workflow.add_edge("tools", "agent")

    return workflow.compile()