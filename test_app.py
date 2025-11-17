# test_app.py

import pytest

# Import the function you want to test
from src.langgraphagenticai.main import load_langgraph_agenticai_app


def test_load_langgraph_agenticai_app_runs():
    """
    Test if the LangGraph Agentic AI app loads without raising an exception.
    """
    try:
        load_langgraph_agenticai_app()
    except Exception as e:
        pytest.fail(f"load_langgraph_agenticai_app() raised an exception: {e}")


if __name__ == "__main__":
    # Run the function manually if executing the test directly
    try:
        print("Running standalone test...")
        load_langgraph_agenticai_app()
        print("Success: App loaded without errors!")
    except Exception as e:
        print(f"Error: {e}")
