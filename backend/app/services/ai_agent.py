import requests
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from datetime import datetime
from app.core.config import settings


@tool
def get_current_server_time() -> str:
    """Returns the current date and time of the server.
    Use this whenever the user asks for the current time, date, or deadline calculations.
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


@tool
def get_github_open_issues(repo_name: str) -> str:
    """Fetches the list of open issues from a specific GitHub repository.
    The repo_name MUST be in the format 'owner/repo' (e.g., 'facebook/react' or 'dineth-panditha/ai-tech-pm').
    Use this when the user asks about pending tasks, open issues, or bugs in a specific repository.
    """

    print(f"----> AI is trying to call GitHub API for repo: {repo_name}...")

    url = f"https://api.github.com/repos/{repo_name}/issues?state=open"
    headers = {
        "Authorization": f"token {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 404:
            return f"Repository '{repo_name}' not found. Please ensure it's in 'owner/repo' format."
        elif response.status_code == 401:
            return "Unauthorized. Please check if the GitHub token is valid."

        response.raise_for_status()
        issues = response.json()

        print(f"----> GitHub API Success! Found {len(issues)} items in {repo_name}.")

        if not issues:
            return (
                f"There are no open issues in '{repo_name}' right now. Great job team!"
            )

        issue_list = []
        for issue in issues:
            if "pull_request" not in issue:
                issue_str = f"ID: {issue['number']}, Title: {issue['title']}"
                issue_list.append(issue_str)

        if issue_list:
            return f"Found {len(issue_list)} open issues in {repo_name}:\n" + "\n".join(
                issue_list
            )
        else:
            return f"No standard open issues found in {repo_name}."

    except Exception as e:
        print(f"---->  GitHub API Error: {str(e)}")
        return f"Failed to fetch GitHub issues for {repo_name}. Error: {str(e)}"


@tool
def get_clickup_tasks() -> str:
    """Fetches the list of active tasks from the ClickUp workspace.
    Use this when the user asks about general project tasks, pending work, or ClickUp tickets.
    """

    print("----> AI is trying to call ClickUp API...")

    url = f"https://api.clickup.com/api/v2/team/{settings.CLICKUP_TEAM_ID}/task"
    headers = {
        "Authorization": settings.CLICKUP_API_TOKEN,
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 401:
            return "Unauthorized. Please check if the ClickUp API token is valid."

        response.raise_for_status()
        data = response.json()
        tasks = data.get("tasks", [])

        print(f"----> ClickUp API Success! Found {len(tasks)} tasks.")

        if not tasks:
            return "There are no active tasks in ClickUp right now."

        task_list = []
        for task in tasks:
            status = task.get("status", {}).get("status", "Unknown")
            assignees = (
                ", ".join([user["username"] for user in task.get("assignees", [])])
                or "Unassigned"
            )

            task_str = (
                f"Task: {task['name']} | Status: {status} | Assignee: {assignees}"
            )
            task_list.append(task_str)

        if task_list:
            return f"Found {len(task_list)} tasks in ClickUp:\n" + "\n".join(task_list)
        else:
            return "No readable tasks found in ClickUp."

    except Exception as e:
        print(f"----> ClickUp API Error: {str(e)}")
        return f"Failed to fetch ClickUp tasks. Error: {str(e)}"

@tool
def create_github_issue(repo_name: str, title: str, body: str) -> str:
    """Creates a new issue in a specific GitHub repository.
    The repo_name MUST be in the format 'owner/repo'.
    Use this when the user asks to create, open, or log a new issue, bug, or task in a GitHub repository."""
    
    print(f"----> AI is trying to create a GitHub issue in {repo_name}...")
    
    url = f"https://api.github.com/repos/{repo_name}/issues"
    headers = {
        "Authorization": f"token {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    payload = {
        "title": title,
        "body": body
    }
    
    try:
       
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 404:
            return f"Repository '{repo_name}' not found. Please ensure it's in 'owner/repo' format."
        elif response.status_code == 401:
            return "Unauthorized. Please check if the GitHub token has 'repo' permissions."
            
        response.raise_for_status() 
        issue_data = response.json()
        
        print(f"----> GitHub API Success! Created issue #{issue_data['number']}.")
        
        return f"Successfully created issue #{issue_data['number']}: '{issue_data['title']}'. URL: {issue_data['html_url']}"
        
    except Exception as e:
        print(f"----> GitHub API Error: {str(e)}")
        return f"Failed to create GitHub issue in {repo_name}. Error: {str(e)}"

    
def get_llm():
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name="llama-3.3-70b-versatile",
        temperature=0.1,
    )


def chat_with_agent(user_message: str):
    print(f"---->  User asked: {user_message}")
    
    llm = get_llm()
    
   
    tools = [get_current_server_time, get_github_open_issues, get_clickup_tasks, create_github_issue]
    
    system_prompt = """You are an expert AI Technical Project Manager. 
    You manage software development teams, their GitHub repositories, and ClickUp tasks.
    
    CRITICAL RULES:
    1. ONLY use the tools explicitly provided to you.
    2. NEVER attempt to use external search tools.
    3. When checking or creating GitHub issues, you MUST provide the 'repo_name' parameter in 'owner/repo' format.
    4. If the user does not specify the repository owner, politely ask them for the full 'owner/repo' format before using the tool.
    5. AFTER using a tool and receiving data, DO NOT call the tool again. Immediately summarize the data and answer the user.
    6. For general project tasks, sprint planning, and tickets, ALWAYS use get_clickup_tasks.
    7. If the user asks to create a bug or issue, use the create_github_issue tool. If they don't provide a title or body, ask them for the details first.
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
