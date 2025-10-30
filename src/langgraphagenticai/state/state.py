from typing_extensions import TypedDict,List
from typing import Annotated
from langgraph.graph import add_messages 

class State(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        messages: A list of messages exchanged in the conversation.
        user_query: The initial query from the user.
        
    """
    messages: Annotated[List, add_messages]