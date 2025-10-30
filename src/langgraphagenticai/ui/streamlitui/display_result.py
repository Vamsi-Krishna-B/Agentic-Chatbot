import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json

class DisplayResult:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

  
        if "messages" not in st.session_state:
            st.session_state["messages"] = []

 
        for msg in st.session_state["messages"]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        if user_message:
            # Store user message
            st.session_state["messages"].append({"role": "user", "content": user_message})
            with st.chat_message("user"):
                st.write(user_message)

            # Generate response based on use case
            if usecase == "Basic Chatbot":
                response = ""
                for event in graph.stream({"messages": ("user", user_message)}, reasoning_format="hidden"):
                    for value in event.values():
                        if "messages" in value:
                            # Collect partial message if streaming
                            msg_content = value["messages"].content
                            response += msg_content

                st.session_state["messages"].append({"role": "assistant", "content": response})

                with st.chat_message("assistant"):
                    st.write(response)
