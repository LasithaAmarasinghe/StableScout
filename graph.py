import operator
from typing import Annotated, TypedDict, Union

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

# Import the tools we built in tools.py
from tools import get_stablecoin_yield, check_risk_metrics

# 1. Define the Shared State
class AgentState(TypedDict):
    # This list will store the entire conversation history
    messages: Annotated[list, operator.add]

def create_stable_scout_graph(api_key: str):
    """
    Constructs the multi-agent graph with specialized nodes for 
    Yield Analysis and Risk Checking.
    """
    
    # 2. Initialize specialized LLMs
    # The Yield Analyst is allowed to fetch APY data
    analyst_llm = ChatGroq(
        model="llama-3.3-70b-versatile", 
        groq_api_key=api_key,
        temperature=0
    ).bind_tools([get_stablecoin_yield])

    # The Risk Agent is allowed to check price and liquidity metrics
    risk_llm = ChatGroq(
        model="llama-3.3-70b-versatile", 
        groq_api_key=api_key,
        temperature=0
    ).bind_tools([check_risk_metrics])

    # 3. Define the Nodes (The "Brain" steps)
    
    def analyst_node(state: AgentState):
        """Focuses on yield opportunities and answering the user's growth questions."""
        response = analyst_llm.invoke(state["messages"])
        return {"messages": [response]}

    def risk_node(state: AgentState):
        """Focuses on verifying the safety of the proposed asset/yield."""
        # System prompt injection to ensure the Risk Agent stays skeptical
        messages = [("system", "You are a specialized Risk Officer. Your only job is to check for de-peg or liquidity issues.")] + state["messages"]
        response = risk_llm.invoke(messages)
        return {"messages": [response]}

    # 4. Define Routing Logic
    
    def should_continue(state: AgentState):
        """Determines if the LLM wants to use a tool or if the conversation is done."""
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            return "tools"
        return "next_agent"

    def route_after_risk(state: AgentState):
        """Determines if we need more tools or can finish after the risk check."""
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            return "tools"
        return END

    # 5. Build the Graph
    workflow = StateGraph(AgentState)

    # Add the specialized worker nodes
    workflow.add_node("yield_analyst", analyst_node)
    workflow.add_node("risk_checker", risk_node)
    
    # Add a unified tool-execution node for all agents
    workflow.add_node("tools", ToolNode([get_stablecoin_yield, check_risk_metrics]))

    # Set up the control flow
    workflow.add_edge(START, "yield_analyst")

    # Analyst Logic: If calling a tool, go to 'tools'. Otherwise, handoff to 'risk_checker'.
    workflow.add_conditional_edges(
        "yield_analyst",
        should_continue,
        {
            "tools": "tools",
            "next_agent": "risk_checker"
        }
    )

    # Risk Logic: If calling a tool, go to 'tools'. Otherwise, finish the report.
    workflow.add_conditional_edges(
        "risk_checker",
        route_after_risk,
        {
            "tools": "tools",
            END: END
        }
    )

    # All tools always return to the node that called them
    # LangGraph intelligently routes back based on the last sender
    workflow.add_edge("tools", "yield_analyst") 

    return workflow.compile()