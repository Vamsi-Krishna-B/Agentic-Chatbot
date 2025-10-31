import streamlit as st 
import os
from src.langgraphagenticai.ui.uiconfigfile import Config 

class LoadStreamlitUI: 
    def __init__(self):
        self.config = Config()
        self.user_controls = {}
        
    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 "+ self.config.get_page_title(),layout="wide")
        st.header("🤖 "+ self.config.get_page_title())
        
        with st.sidebar:
            # Get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_use_case_options()
            
            # LLM selection
            self.user_controls['selected_llm'] = st.selectbox("Select LLM",llm_options)
            
            if self.user_controls['selected_llm'] == 'Groq':
                
                # Model selection
                model_options = self.config.get_groq_model_options()
                self.user_controls['selected_groq_model'] = st.selectbox("Select Model",model_options) 
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API Key",type="password")
                
                # Validate API Key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠️ Please provide your Groq API key to proceed!!")
                    
            self.user_controls['selected_usecase'] = st.selectbox("Select Use Case",usecase_options)
            
            if self.user_controls['selected_usecase'] == 'Chatbot with tools' or self.user_controls['selected_usecase'] == 'AI News' :
                os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("Tavily API Key",type="password")
                if self.user_controls["TAVILY_API_KEY"] == '':
                    st.warning("⚠️ Please provide your Tavily API key to proceed!!")
                if self.user_controls['selected_usecase'] == "AI News":
                    st.subheader("📰 AI News Explorer")
                    with st.sidebar:
                        time_frame = st.selectbox(
                            "🗓️ Select Time Frame",
                            ["Daily","Weekly","Monthly","Yearly"],
                            index=0
                        )   
                    if st.button("🔍 Fetch Latest AI News",use_container_width=True):
                        st.session_state.IsFetchButtonClicked = True 
                        st.session_state.time_frame = time_frame
        return self.user_controls
            