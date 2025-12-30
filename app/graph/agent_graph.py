
from app.graph.nodes import chatbot
from app.graph.nodes import AgentState, tools

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition


# Build the graph
builder = StateGraph(AgentState)

# Add nodes
builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools))

# Add edges
builder.add_edge(START, "chatbot")

# Conditional edge: check if the LLM requested a tool
builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

# Return from tools back to chatbot
builder.add_edge("tools", "chatbot")

# Compile the graph
graph = builder.compile()

def get_graph():
    return graph
