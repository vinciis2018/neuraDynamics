from app.tools.weather_tool import get_weather
from app.tools.rag_tool import ask_document
import pytest
from unittest.mock import patch, MagicMock
import os

# Set dummy API key for tests before importing graph
os.environ["OPENAI_API_KEY"] = "test-key"
os.environ["OPENWEATHERMAP_API_KEY"] = "test-weather-key"

@patch('app.tools.weather_tool.requests.get')
def test_weather_tool_success(mock_get):
    """Test the weather tool parses successful API response correctly."""
    # Mock response data
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'weather': [{'description': 'sunny'}],
        'main': {'temp': 25, 'feels_like': 27, 'humidity': 50}
    }
    mock_get.return_value = mock_response

    # Call the tool directly (bypassing the decoration for simplicity if needed, but tool is callable)
    result = get_weather.invoke("London")
    
    assert "sunny" in result
    assert "25" in result

@patch('app.tools.weather_tool.requests.get')
def test_weather_tool_failure(mock_get):
    """Test the weather tool handles API errors gracefully."""
    mock_get.side_effect = Exception("API Down")
    
    result = get_weather.invoke("Unknown City")
    assert "An error occurred" in result

@patch('app.tools.rag_tool.ingest_and_get_retriever')
def test_rag_tool(mock_ingest):
    """Test the RAG tool logic (mocking the retriever)."""
    # Create the mock retriever
    mock_retriever = MagicMock()
    mock_doc = MagicMock()
    mock_doc.page_content = "LangGraph is a library."
    mock_retriever.invoke.return_value = [mock_doc]
    
    mock_ingest.return_value = mock_retriever
    
    # We need to ensure _RETRIEVER is reset or mocked in the module for this test to isolate it
    # But since we are patching ingest_and_get_retriever, if get_retriever calls it, we are good.
    # Ideally we'd reset the global variable in the module too.
    with patch('app.tools.rag_tool._RETRIEVER', None):
        result = ask_document.invoke("What is LangGraph?")
        assert "LangGraph is a library" in result

# Integration test placeholder
def test_graph_compilation():
    from app.graph.agent_graph import get_graph
    graph = get_graph()
    assert graph is not None
