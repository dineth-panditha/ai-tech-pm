import requests
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

@tool
def get_github_open_issues() -> str:
    """Fetches the list of open issues from the GitHub repository. 
    Use this when the user asks about pending tasks, open issues, or bugs in the repository."""
    print("----> 🔍 AI is trying to call GitHub API...")
    
    url = f"https://api.github.com/repos/{settings.GITHUB_REPO}/issues?state=open"
    headers = {
        "Authorization": f"token {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
        issues = response.json()
        
        print(f"---->  GitHub API Success! Found {len(issues)} items.")
        
        if not issues:
            return "There are no open issues in the repository right now. Great job team!"
            
        issue_list = []
        for issue in issues:
            if "pull_request" not in issue:
                issue_list.append(f"- Issue #{issue['number']}: {issue['title']} (Assigned to: {issue['assignee']['login'] if issue['assignee'] else 'Unassigned'})")
                
        return "\n".join(issue_list) if issue_list else "No standard open issues found."
        
    except Exception as e:
        print(f"---->  GitHub API Error: {str(e)}")
        return f"Failed to fetch GitHub issues. Error: {str(e)}"
    
def get_llm():
    return ChatGroq(
        api_key=settings.GROQ_API_KEY, 
        model_name="llama-3.3-70b-versatile",
        temperature=0.1 
    )

def chat_with_agent(user_message: str):
    print(f"----> User asked: {user_message}")
    
    llm = get_llm()
    tools = [get_current_server_time, get_github_open_issues]
    
    system_prompt = """You are an expert AI Technical Project Manager. 
    You manage software development teams and their GitHub repositories.
    
    CRITICAL RULES:
    1. ONLY use the tools explicitly provided to you (get_current_server_time, get_github_open_issues).
    2. NEVER attempt to use 'brave_search' or any other external search tools.
    3. If asked about tasks, issues, or bugs, ALWAYS use the get_github_open_issues tool.
    """
    
    agent = create_react_agent(llm, tools)
    print("----> AI is thinking...")

    config = {"recursion_limit": 5}

    response = agent.invoke({
        "messages": [
            ("system", system_prompt),
            ("user", user_message)
        ]
    }, config=config)

    print("----> AI finished thinking!")
    
    return response["messages"][-1].content