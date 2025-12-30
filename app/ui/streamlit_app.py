import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure app is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.graph.agent_graph import get_graph
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(page_title="AI Pipeline Agent", layout="wide")

st.title("LangGraph AI Agent")
st.markdown("Ask me anything about the **Weather** or the **internal Knowledge Base**.")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# Input for user query
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to state
    user_msg = HumanMessage(content=prompt)
    st.session_state.messages.append(user_msg)
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Trigger Agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                graph = get_graph()
                # Run the graph with the full history or just the new message
                # For this simple agent, passing full history is good context.
                # Note: The graph expects a dict with "messages" key.
                inputs = {"messages": st.session_state.messages}
                
                # Stream results or invoke
                # If we stream, we can get intermediate steps, but invoke is simpler for now.
                response = graph.invoke(inputs)
                
                # Get the last message from the agent
                final_msg = response["messages"][-1]
                st.markdown(final_msg.content)
                
                # Append to session state
                st.session_state.messages.append(final_msg)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Sidebar
with st.sidebar:
    st.header("Debug Info")
    if st.checkbox("Show Graph Visualization"):
        st.info("Graph visualization requires mermaid-js integration or standard output.")
    
    st.markdown("---")
    st.markdown("Built with LangGraph, Qdrant, and Streamlit.")
