from src.langgraphagenticai.state.state import State
from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate


class AiNewsNode:
    """
    Chatbot with tool help
    """
    def __init__(self,model):
        self.tavily = TavilyClient()
        self.llm = model
        self.state
    def fetch_news(self,state:dict)->dict:
        """
        Fetch AI News based on the specified frequency 
        
        Args:
            state (dict): The state dictionary containing frequency.
        Returns:
            dict:updated state with 'news_data' key containing the fetched news data.
        """
        
        frequency = state["messages"][0].content.lower()
        self.state['frequency'] = frequency 
        time_range_map = {
            "daily":"d",
            "weekly":"w",
            "monthly":"m",
            "yearly":"y"
        }
        days_map = {
            "daily":1,
            "weekly":7,
            "monthly":30,
            "yearly":365
        }
        response = self.tavily.search(
            query="Top Artificail Intelligence (AI) News India and Globally.",
            topic="news",
            time_range = time_range_map[frequency],
            include_answer="advanced",
            max_results=15,
            days = days_map[frequency]
        )
        state['news_data'] = response.get('results',[])
        self.state['news_data'] = state['news_data']
        return state
    def summarize_news(self,state:dict)->dict:
        """
        Summarizes the fetched news data.
        Args:
            state (dict): The state dictionary containing 'news_data'.
        Returns:
            dict: Updated state with 'summaries' key containing the summarized news.
        """
        news_item = self.state['news_data']
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system","""Summarize AI news articles into a markdown format. For each item include:
                 -Date in **YYYY-MM-DD** format in IST timezone
                 -concise sentences summary from latest news
                 -sort news by date wise (latest first)
                 -source URL as link
                 Use format:
                 ### [Date]
                 -[Summary](URL)
                 """),
                
                ("user","Article:\n{articles}")
            ]
        )
        articles_str = "\n\n".join([
            f"Content: {item.get('content','')}\n URL: {item.get('url','')} \n Date: {item.get('published_date','')}" 
            for item in news_item
        
        ])
        
        response = self.llm.invoke(prompt.format(articles=articles_str),reasoning_format="hidden")
        state['summary'] = response.content 
        self.state['summary'] = state['summary']
        return self.state
    
    def save_results(self,state:dict)->dict:
        """
        Saves the summarized news to a markdown file.
        Args:
            state (dict): The state dictionary containing 'summary' and 'frequency'.
        Returns:
            dict: Updated state with 'file_path' key containing the path to the saved file.
        """
        summary = self.state['summary']
        frequency = self.state['frequency']
        file_name = f"./AI_News/ai_news_{frequency.lower()}.md"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(f"#{frequency.capitalize()} AI News Summary \n\n")
            f.write(summary)
        state['file_name'] = file_name
        return self.state
        