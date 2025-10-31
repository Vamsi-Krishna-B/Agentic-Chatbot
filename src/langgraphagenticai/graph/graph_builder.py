from langgraph.graph import StateGraph,START,END
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.nodes.chatbot_with_tools_node import ChatbotWithToolsNode
from src.langgraphagenticai.tools.search_tool import get_tools,create_tools_node
from langgraph.prebuilt import tools_condition
from src.langgraphagenticai.nodes.ai_news_node import AiNewsNode

class GraphBuilder:
    def __init__(self,model):
        self.llm = model 
        self.graph_builder = StateGraph(State)
    
    def basic_chatbot_build_graph(self):
        """
        
        Builds a basic chatbot graph using Langgraph.
        This method initializes a chatbot sing the 'BasicChatbotNode' class
        and integrates it into the graph. The chatbot node is set as both the 
        entry and exit point of the graph.
        
        """
        self.basic_chatbot_node = BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)
    
    def chatbot_with_tools_build_graph(self):
        """
        Builds a chatbot with tool which will be helpful in 
        making relevant calls and make beter responses.Then the node is integrated
        into the graph.This node is set as both the entry and exit point of the graph.
        """
        tools = get_tools()
        tools_node = create_tools_node(tools)
        
        self.chatbot_with_tools_node = ChatbotWithToolsNode(self.llm)
        chatbot_node = self.chatbot_with_tools_node.create_chatbot(tools)
        self.graph_builder.add_node("chatbot_with_tools",chatbot_node)
        self.graph_builder.add_node("tools",tools_node)
        self.graph_builder.add_edge(START,"chatbot_with_tools")
        self.graph_builder.add_conditional_edges("chatbot_with_tools",tools_condition)
        self.graph_builder.add_edge("tools","chatbot_with_tools")
        self.graph_builder.add_edge("chatbot_with_tools",END)
        
    def ai_news_build_graph(self):
        """
        Builds a chatbot which fetches the AI news based using API calls 
        filtered according to the time frame specified.
        """
        ai_news_node = AiNewsNode(self.llm)
        self.graph_builder.add_node("fetch_news",ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize",ai_news_node.summarize_news)
        self.graph_builder.add_node("save_results",ai_news_node.save_results)
        
        
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news","summarize")
        self.graph_builder.add_edge("summarize","save_results")
        self.graph_builder.add_edge("save_results",END)
        
        
        
    def setup_graph(self,usecase:str):
        """
            Sets up the graph for the selected use case
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        elif usecase == "Chatbot with tools":
            self.chatbot_with_tools_build_graph()
        elif usecase == "AI News":
            self.ai_news_build_graph()
            
        return self.graph_builder.compile()