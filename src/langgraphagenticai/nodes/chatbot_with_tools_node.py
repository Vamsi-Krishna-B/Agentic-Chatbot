
from src.langgraphagenticai.state.state import State


class ChatbotWithToolsNode:
    """
    Chatbot with tool help
    """
    def __init__(self,model):
        self.llm = model
    
    def create_chatbot(self,tools):
        """
        Returns a chatbot node function.
        Args:
            tools (_type_): _description_
        """
        llm_with_tools = self.llm.bind_tools(tools)
        def chatbot_node(state:State):
            """
            Chatbot logic for processing the input state and returning a response. 
            """
            return {"messages":llm_with_tools.invoke(state["messages"],reasoning_format="hidden")}
        return chatbot_node