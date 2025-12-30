# LangGraph AI Pipeline

This project demonstrates an agentic AI pipeline using LangGraph, LangChain, and Qdrant. The agent can fetch real-time weather data and answer questions from a PDF knowledge base using RAG.

## Features
- **Agentic Workflow**: Uses LangGraph to route queries to the appropriate tool (Weather or Knowledge Base).
- **RAG System**: Ingests a PDF, creates embeddings, and retrieves relevant info using Qdrant.
- **Tools**:
  - `get_weather`: Fetches live weather from OpenWeatherMap.
  - `ask_document`: Retrieves context from the internal knowledge base.
- **UI**: A Streamlit chat interface for easy interaction.
- **Evaluation**: Integrated with LangSmith for tracing and evaluation.

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Copy `.env.example` to `.env` and fill in your keys:
   ```bash
   cp .env.example .env
   ```
   Required Keys:
   - `OPENAI_API_KEY`
   - `OPENWEATHERMAP_API_KEY`
   - `LANGCHAIN_API_KEY` (for LangSmith)

5. **Generate Knowledge Base**:
   Run the script to create the dummy PDF (if not already present):
   ```bash
   python generate_pdf.py
   ```

## Usage

### Run the Streamlit App
```bash
streamlit run app/ui/streamlit_app.py
```

### Run Tests
```bash
pytest tests/
```

## Architecture
- **Graph**: `app/graph/agent_graph.py` defines the state machine.
- **Tools**: `app/tools/` contains the Weather and RAG tools.
- **Vector Store**: `app/vector_store/` handles Qdrant interactions.

## Evaluation
Logs and traces are sent to LangSmith project `weather-rag-agent`. Check the LangSmith dashboard for detailed run information.
