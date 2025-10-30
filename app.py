from src.langgraphagenticai.main import load_langgraph_agenticai_app
import streamlit as st
if __name__ == "__main__":
    try:
        load_langgraph_agenticai_app()
    except Exception as e:
        st.error(f"An error occurred: {e}")