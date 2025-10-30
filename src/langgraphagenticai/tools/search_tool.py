from langchain_tavily import TavilySearch 
from langgraph.prebuilt import ToolNode 

def get_tools():
    """
    Return the list of tools to be used in the chatbot 
    """
    tools = [TavilySearch(max_results=2)]
    return tools

def create_tools_node(tools):
    """
    create and returns a tool node for the graph 
    """
    return ToolNode(tools=tools)