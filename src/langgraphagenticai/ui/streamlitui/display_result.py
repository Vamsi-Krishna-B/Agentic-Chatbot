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
            elif usecase == "Chatbot with tools":
            # ✅ Prepare initial state and invoke graph
                initial_state = {"messages": [user_message]}
                res = graph.invoke(initial_state, reasoning_format="hidden")
    
                for message in res["messages"]:
                    # Human Message
                    if isinstance(message, HumanMessage):
                        role = "user"
                        content = message.content
                    # Tool Message
                    elif isinstance(message, ToolMessage):
                        role = "assistant"
                        content = f"🧰 **Tool Call Start**\n\n{message.content}\n\n🧰 **Tool Call End**"
                    # AI Message
                    elif isinstance(message, AIMessage) and message.content:
                        role = "assistant"
                        content = message.content
                    else:
                        continue
                    
                    # ✅ Display message
                    with st.chat_message(role):
                        st.write(content)
    
                    # ✅ Append to session history
                    st.session_state["messages"].append({"role": role, "content": content})

            elif usecase == "AI News":
                    frequency = self.user_message
                
                    # ✅ Display user message and add to chat history
                    st.session_state["messages"].append({"role": "user", "content": frequency})
                    with st.chat_message("user"):
                        st.write(frequency)
                
                    # ✅ Processing spinner
                    with st.spinner("Fetching and Summarizing AI News..."):
                        try:
                            # Invoke your AI news graph
                            result = graph.invoke({"messages": frequency})
                
                            # Construct expected markdown path
                            AI_NEWS_PATH = f"./AI_News/ai_news_{frequency.lower()}.md"
                
                            # ✅ Read and display markdown content
                            with open(AI_NEWS_PATH, "r", encoding="utf-8") as f:
                                markdown_content = f.read()
                
                            with st.chat_message("assistant"):
                                st.markdown(markdown_content, unsafe_allow_html=True)
                
                            # ✅ Add assistant message to session history
                            st.session_state["messages"].append({
                                "role": "assistant",
                                "content": markdown_content
                            })
                
                        except FileNotFoundError:
                            error_msg = f"❌ The file `{AI_NEWS_PATH}` was not found. Please ensure the news has been fetched and summarized correctly."
                            with st.chat_message("assistant"):
                                st.error(error_msg)
                            st.session_state["messages"].append({"role": "assistant", "content": error_msg})
                
                        except Exception as e:
                            error_msg = f"⚠️ An error occurred: {str(e)}"
                            with st.chat_message("assistant"):
                                st.error(error_msg)
                            st.session_state["messages"].append({"role": "assistant", "content": error_msg})

                   
