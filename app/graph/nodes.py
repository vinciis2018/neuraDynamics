
from typing import Annotated, Literal, TypedDict
from langchain_openai import ChatOpenAI

from app.tools.weather_tool import get_weather
from app.tools.rag_tool import ask_document
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langgraph.graph.message import add_messages

# Define the state
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Define tools
tools = [get_weather, ask_document]

# Create the agent model
llm = ChatOpenAI(model="gpt-5-mini").bind_tools(tools)


# Define nodes
def chatbot(state: AgentState):
    """
    Main agent node that decides what to do next.
    """
    system_prompt = SystemMessage(content="You are a helpful assistant. You have access to a Knowledge Base (PDF) that contains information about various topics including cyclones, history, and technical documentation. ALWAYS use the 'ask_document' tool if the user asks a question that might be answered by this knowledge base, essentially acting as a RAG system. Do not hallucinate if you can check the document.")
    
    messages = [system_prompt] + state["messages"]
    return {"messages": [llm.invoke(messages)]}
