import requests
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from datetime import datetime
from app.core.config import settings
from supabase import create_client, Client

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


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


# --- Dynamic ClickUp Tools ---


@tool
def get_clickup_workspaces() -> str:
    """Fetches all ClickUp workspaces (teams) the user has access to.
    Always use this first to find the 'team_id' before looking for spaces or tasks."""
    print("----> AI is fetching ClickUp Workspaces...")
    url = "https://api.clickup.com/api/v2/team"
    headers = {"Authorization": settings.CLICKUP_API_TOKEN}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        teams = response.json().get("teams", [])

        if not teams:
            return "No Workspaces found."

        result = "ClickUp Workspaces (Teams):\n"
        for t in teams:
            result += f"- ID: {t['id']} | Name: {t['name']}\n"
        return result
    except Exception as e:
        return f"Error fetching workspaces: {str(e)}"


@tool
def get_clickup_spaces(team_id: str) -> str:
    """Fetches all Spaces within a specific ClickUp Workspace (team_id).
    Use this to find the 'space_id' before creating lists or tasks."""
    print(f"----> AI is fetching Spaces for Team: {team_id}...")
    url = f"https://api.clickup.com/api/v2/team/{team_id}/space"
    headers = {"Authorization": settings.CLICKUP_API_TOKEN}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        spaces = response.json().get("spaces", [])

        if not spaces:
            return f"No Spaces found in workspace {team_id}."

        result = f"Spaces in Workspace {team_id}:\n"
        for s in spaces:
            result += f"- ID: {s['id']} | Name: {s['name']}\n"
        return result
    except Exception as e:
        return f"Error fetching spaces: {str(e)}"


@tool
def get_clickup_lists(space_id: str) -> str:
    """Fetches all Lists within a specific ClickUp Space (space_id).
    Use this to find the 'list_id' before creating tasks."""
    print(f"----> AI is fetching Lists for Space: {space_id}...")
    url = f"https://api.clickup.com/api/v2/space/{space_id}/list"
    headers = {"Authorization": settings.CLICKUP_API_TOKEN}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        lists = response.json().get("lists", [])

        if not lists:
            return f"No Lists found in space {space_id}."

        result = f"Lists in Space {space_id}:\n"
        for l in lists:
            result += f"- ID: {l['id']} | Name: {l['name']}\n"
        return result
    except Exception as e:
        return f"Error fetching lists: {str(e)}"


@tool
def create_clickup_space(team_id: str, space_name: str) -> str:
    """Creates a new Space in a specific ClickUp Workspace (team_id)."""
    print(f"----> AI is creating Space '{space_name}'...")
    url = f"https://api.clickup.com/api/v2/team/{team_id}/space"
    headers = {
        "Authorization": settings.CLICKUP_API_TOKEN,
        "Content-Type": "application/json",
    }
    payload = {"name": space_name, "multiple_assignees": True}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        space = response.json()
        return f"Successfully created Space '{space['name']}' with ID: {space['id']}"
    except Exception as e:
        return f"Error creating space: {str(e)}"


@tool
def create_clickup_list(space_id: str, list_name: str) -> str:
    """Creates a new List in a specific ClickUp Space (space_id)."""
    print(f"---->  AI is creating List '{list_name}'...")
    url = f"https://api.clickup.com/api/v2/space/{space_id}/list"
    headers = {
        "Authorization": settings.CLICKUP_API_TOKEN,
        "Content-Type": "application/json",
    }
    payload = {"name": list_name}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        new_list = response.json()
        return (
            f"Successfully created List '{new_list['name']}' with ID: {new_list['id']}"
        )
    except Exception as e:
        return f"Error creating list: {str(e)}"


@tool
def create_clickup_task(list_id: str, task_name: str, description: str = "") -> str:
    """Creates a new Task in a specific ClickUp List (list_id)."""
    print(f"----> AI is creating Task '{task_name}'...")
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    headers = {
        "Authorization": settings.CLICKUP_API_TOKEN,
        "Content-Type": "application/json",
    }
    payload = {"name": task_name, "description": description, "status": "TO DO"}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        task = response.json()
        return f"Successfully created Task '{task['name']}' with ID: {task['id']}. URL: {task['url']}"
    except Exception as e:
        return f"Error creating task: {str(e)}"


@tool
def create_github_issue(repo_name: str, title: str, body: str) -> str:
    """Creates a new issue in a specific GitHub repository.
    The repo_name MUST be in the format 'owner/repo'.
    Use this when the user asks to create, open, or log a new issue, bug, or task in a GitHub repository.
    """
    print(f"----> AI is trying to create a GitHub issue in {repo_name}...")

    url = f"https://api.github.com/repos/{repo_name}/issues"
    headers = {
        "Authorization": f"token {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    payload = {"title": title, "body": body}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)

        if response.status_code == 404:
            return f"Repository '{repo_name}' not found. Please ensure it's in 'owner/repo' format."
        elif response.status_code == 401:
            return (
                "Unauthorized. Please check if the GitHub token has 'repo' permissions."
            )

        response.raise_for_status()
        issue_data = response.json()

        print(f"----> GitHub API Success! Created issue #{issue_data['number']}.")

        return f"Successfully created issue #{issue_data['number']}: '{issue_data['title']}'. URL: {issue_data['html_url']}"

    except Exception as e:
        print(f"----> GitHub API Error: {str(e)}")
        return f"Failed to create GitHub issue in {repo_name}. Error: {str(e)}"


@tool
def save_project_note(title: str, content: str) -> str:
    """Saves an important project note, decision, or meeting summary to the database.
    Use this when the user asks you to remember something, save a note, or document a decision.
    """

    print(f"----> AI is saving a note to Supabase: {title}")

    try:
        data, count = (
            supabase.table("project_notes")
            .insert({"title": title, "content": content})
            .execute()
        )
        return f"Successfully saved the note '{title}' to the database."
    except Exception as e:
        print(f"----> Supabase Insert Error: {str(e)}")
        return f"Failed to save the note. Error: {str(e)}"


@tool
def get_project_notes() -> str:
    """Retrieves all saved project notes, decisions, and summaries from the database.
    Use this when the user asks what you remember, what was discussed before, or asks for project notes.
    """

    print("----> AI is reading notes from Supabase...")

    try:
        response = (
            supabase.table("project_notes")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        notes = response.data

        if not notes:
            return "There are no saved notes in the database yet."

        note_list = []
        for note in notes:
            note_list.append(f"- **{note['title']}**: {note['content']}")

        return "Here are the saved project notes:\n" + "\n".join(note_list)
    except Exception as e:
        print(f"----> Supabase Select Error: {str(e)}")
        return f"Failed to retrieve notes. Error: {str(e)}"



@tool
def send_discord_message(message: str) -> str:
    """Sends a message to the team's Discord channel.
    Use this to notify the team about new tasks, decisions, or important updates."""
    print(f"----> AI is sending a message to Discord: {message}")
    
    url = settings.DISCORD_WEBHOOK_URL
    payload = {
        "content": message,
        "username": "AI Project Manager", 
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/8617/8617156.png" # ලස්සන රොබෝ අයිකන් එකක්
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return "Message successfully sent to Discord."
    except Exception as e:
        return f"Failed to send message to Discord: {str(e)}"

# --- DevOps & Code Review Tools ---

@tool
def get_github_pr_diff(repo_name: str, pr_number: int) -> str:
    """Fetches the code diff of a GitHub Pull Request.
    repo_name format: 'owner/repo'. Use this to read the code changes before reviewing."""
    print(f"----> AI is fetching PR #{pr_number} diff from {repo_name}...")
    url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}"
    
    # Accept header එක '.diff' විදියට දීම අනිවාර්යයි කෝඩ් වෙනස්කම් ගන්න නම්
    headers = {
        "Authorization": f"token {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff" 
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        diff = response.text
        
        
        if len(diff) > 4000:
            return diff[:4000] + "\n... [Diff truncated due to length]"
        return diff
    except Exception as e:
        return f"Error fetching PR diff: {str(e)}"

@tool
def post_github_pr_comment(repo_name: str, pr_number: int, comment: str) -> str:
    """Posts a comment or review on a GitHub Pull Request.
    repo_name format: 'owner/repo'. Use this to post your code review feedback."""
    print(f"----> AI is posting a review on PR #{pr_number}...")
    url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.post(url, headers=headers, json={"body": comment}, timeout=10)
        response.raise_for_status()
        return f"Successfully posted code review to PR #{pr_number}."
    except Exception as e:
        return f"Error posting comment: {str(e)}"

@tool
def check_github_actions_status(repo_name: str) -> str:
    """Checks the latest GitHub Actions (CI/CD) workflow runs for a repository.
    repo_name format: 'owner/repo'. Use this to check if builds are passing."""
    print(f"---->AI is checking CI/CD status for {repo_name}...")
    url = f"https://api.github.com/repos/{repo_name}/actions/runs?per_page=3"
    headers = {
        "Authorization": f"token {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        runs = response.json().get("workflow_runs", [])
        
        if not runs:
            return "No GitHub Actions workflows found."
            
        result = f"Latest CI/CD Runs for {repo_name}:\n"
        for run in runs:
            result += f"- Name: {run['name']} | Branch: {run['head_branch']} | Status: {run['status']} | Conclusion: {run['conclusion']}\n"
        return result
    except Exception as e:
       return f"Error checking CI/CD status: {str(e)}"


    
# --- RAG & Enterprise Knowledge Tools ---

def get_text_embedding(text: str) -> list:
    """Helper function to convert text into a 384-dimensional vector using Hugging Face."""
    model_id = "sentence-transformers/all-MiniLM-L6-v2"
    url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
    headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}
    
    response = requests.post(url, headers=headers, json={"inputs": text}, timeout=15)
    response.raise_for_status()
    return response.json()

@tool
def save_project_document(title: str, content: str) -> str:
    """Saves a project document (architecture, guidelines, ideas) to the AI's long-term vector memory.
    Use this to memorize important project information for the future."""
    print(f"---->  AI is learning and saving a new document: {title}...")
    try:
        # Convert text to vector embedding
        vector = get_text_embedding(content)
        
        # Save to Supabase pgvector database
        data = {
            "content": content,
            "metadata": {"title": title},
            "embedding": vector
        }
        
        
        supabase.table("project_documents").insert(data).execute()
        return f"Successfully saved and memorized the document: '{title}'"
    except Exception as e:
        return f"Error saving document: {str(e)}"

@tool
def search_project_documents(query: str) -> str:
    """Searches the project documentation for information related to the query.
    Use this when you need to recall project rules, architecture, or past documentation."""
    print(f"---->  AI is searching memory for: {query}...")
    try:
        # Convert search query to vector
        query_vector = get_text_embedding(query)
        
        # Perform similarity search using Supabase RPC
       
        response = supabase.rpc(
            "match_documents",
            {
                "query_embedding": query_vector, 
                "match_threshold": 0.3, 
                "match_count": 3        
            }
        ).execute()
        
        results = response.data
        if not results:
            return "No relevant documents found in memory."
            
        context = "Found the following relevant documents:\n\n"
        for row in results:
            doc_title = row.get("metadata", {}).get("title", "Unknown")
            context += f"--- Document: {doc_title} ---\n{row.get('content')}\n\n"
            
        return context
    except Exception as e:
        return f"Error searching documents: {str(e)}"

        

# def get_llm():
#     return ChatGroq(
#         api_key=settings.GROQ_API_KEY,
#         model_name="llama-3.1-8b-instant",
#         temperature=0.1,
#     )

def get_llm():
    url = "https://api.groq.com/openai/v1/models"
    headers = {"Authorization": f"Bearer {settings.GROQ_API_KEY}"}
    
    try:
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        models_data = response.json().get("data", [])
        available_models = [m["id"] for m in models_data]
        
        print(f"---->  Available Models in your account: {available_models}")
        
        
        tool_supported_models = [
            "llama3-groq-70b-8192-tool-use-preview",
            "llama3-groq-8b-8192-tool-use-preview",
            "llama3-70b-8192",
            "llama3-8b-8192",
            "llama-3.2-90b-text-preview",
            "llama-3.2-11b-vision-preview",
            "llama-3.2-3b-preview",
            "llama-3.2-1b-preview"
        ]
        
        active_model = None
        
        
        for model in tool_supported_models:
            if model in available_models:
                active_model = model
                break
                
        
        if not active_model:
            for m in available_models:
                if "llama" in m.lower() and "guard" not in m.lower():
                    active_model = m
                    break
                    
        
        if not active_model:
            active_model = available_models[0]
            
        print(f"----> Successfully Selected Tool-Calling Model: {active_model}")
        
    except Exception as e:
        print(f"----> API Error fetching models: {e}")
        active_model = "llama3-8b-8192"

    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name=active_model,
        temperature=0.1,
    )



def chat_with_agent(user_message: str):
    print(f"---->  User asked: {user_message}")

    llm = get_llm()

    tools = [
        get_current_server_time, get_github_open_issues, create_github_issue,
        save_project_note, get_project_notes,
        get_clickup_workspaces, get_clickup_spaces, get_clickup_lists,
        create_clickup_space, create_clickup_list, create_clickup_task,
        send_discord_message,
        get_github_pr_diff, post_github_pr_comment, check_github_actions_status,
        save_project_document,
        search_project_documents
    ]

    system_prompt = """You are an expert AI Technical Project Manager and Tech Lead. 
    You manage software development teams, GitHub repositories, ClickUp, and project documentation.
    
    CRITICAL RULES:
    1. ONLY use the tools explicitly provided to you.
    2. ClickUp Workflow: You must dynamically find IDs before creating tasks.
    3. Code Reviews: Read code using get_github_pr_diff before posting reviews.
    4. Enterprise Knowledge (RAG): If the user asks about project architecture, coding guidelines, or historical decisions, use search_project_documents to find the context. If the user gives you a new rule or architecture plan, use save_project_document to memorize it.
    """

    agent = create_react_agent(llm, tools)
    print("----> AI is thinking...")

    config = {"recursion_limit": 15}

    response = agent.invoke(
        {"messages": [("system", system_prompt), ("user", user_message)]}, config=config
    )

    print("----> AI finished thinking!")

    return response["messages"][-1].content
