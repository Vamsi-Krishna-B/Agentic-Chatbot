import streamlit as st 

from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResult

def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph Agentic AI application with Streamlit UI.
    This function initializes the UI,  handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while
    implementing exception handling for robustness.
    
    """
    # Load UI 
    ui = LoadStreamlitUI()
    user_inputs = ui.load_streamlit_ui()
    
    if not user_inputs:
        st.error("Error: Failed to load user input from the UI")
        return
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.time_frame
    else:
        user_message = st.chat_input("Enter your message:")
    
    if user_message:
        try:
            obj_llm_config = GroqLLM(user_controls_input=user_inputs)
            model = obj_llm_config.get_llm_model()
            
            if not model:
                st.error("Error: Failed to get the LLM model")
                return
            usecase = user_inputs.get('selected_usecase')
            if not usecase:
                st.error("Error: No use case selected")
                return
            graph_builder = GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResult(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error setting up the graph: {e}")
                return
            
        except Exception as e:
            raise ValueError(f"Error occured with exception: {e}")