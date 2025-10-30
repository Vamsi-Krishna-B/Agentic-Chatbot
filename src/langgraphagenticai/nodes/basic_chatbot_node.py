from src.langgraphagenticai.state.state import State


class BasicChatbotNode:
    """
    Basic chatbot logic implementation 
    """
    def __init__(self,model):
        self.llm = model 
    
    def process(self,state:State)->dict:
        """
        Processes the input state and returns the output state.    
        """
        return {"messages":self.llm.invoke(state["messages"],reasoning_format="hidden")}