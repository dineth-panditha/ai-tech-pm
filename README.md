<div align="center">
  <h1>🤖 AI Tech Project Manager</h1>
  <p><em>An intelligent, autonomous AI Technical Project Manager built using a ReAct Agentic Workflow.</em></p>

  <!-- Tech Badges -->
  <img src="https://img.shields.io/badge/Next.js-black?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white" alt="Supabase" />
</div>

<br />

This AI assistant integrates with industry-standard development tools to manage tasks, review code, track CI/CD pipelines, and maintain a vector-based long-term project memory (RAG).

---

## 🚀 Features

* **🧠 Autonomous Agent (ReAct):** Powered by LangGraph and Groq, the AI dynamically decides which tools to use based on the user's prompt to solve complex, multi-step problems.
* **🐙 GitHub Integration:** Reads PR diffs, posts code review comments, checks CI/CD Action statuses, and manages open issues.
* **✅ ClickUp Automation:** Dynamically fetches workspace/space/list IDs and creates tasks automatically.
* **📚 Enterprise Knowledge (RAG):** Uses Hugging Face embeddings and Supabase pgvector to memorize and retrieve backend guidelines, architecture rules, and project notes.
* **💬 Discord Notifications:** Sends automated updates and alerts to team channels via webhooks.
* **🎨 Modern UI:** A responsive, Next.js-based chat interface with markdown support, loading states, and quick action suggestions.

---

## 🏗️ System Architecture

*GitHub automatically renders the interactive diagram below.*

```mermaid
graph TD
    %% Frontend
    Client[Next.js Frontend UI] -->|REST API / POST| API[FastAPI Backend]
    
    %% Backend & Agent
    subgraph Core AI Agent
        API --> Agent[LangGraph ReAct Agent]
        Agent <-->|LLM Routing & Reasoning| Groq[Groq API <br/> openai/gpt-oss]
    end
    
    %% Tools & Integrations
    subgraph External Tools & Integrations
        Agent -->|Embeddings| HF[Hugging Face API]
        HF -->|Vector Search & Store| DB[(Supabase pgvector <br/> Project Memory)]
        Agent -->|Task Management| ClickUp[ClickUp API]
        Agent -->|Code Review & CI/CD| GitHub[GitHub API]
        Agent -->|Alerts| Discord[Discord Webhook]
    end


