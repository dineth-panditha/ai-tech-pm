from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from datetime import datetime
from app.core.config import settings

@tool
def get_current_server_time() -> str:
    """Returns the current date and time of the server. 
    Use this whenever the user asks for the current time, date, or deadline calculations."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def get_llm():
    return ChatGroq(
        api_key=settings.GROQ_API_KEY, 
        model_name="llama-3.1-8b-instant", 
        temperature=0.2 
    )


def chat_with_agent(user_message: str):
    llm = get_llm()
    tools = [get_current_server_time]
    
   
    system_prompt = "You are an expert AI Technical Project Manager. You help software development teams manage their workflow. You have access to tools. Always use them if you need real-time data."
    
   
    agent = create_react_agent(llm, tools)
    
    response = agent.invoke({
        "messages": [
            ("system", system_prompt),
            ("user", user_message)
        ]
    })
    
    
    return response["messages"][-1].content