import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings

def get_llm():
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name="llama-3.1-8b-instant",
        temperature=0.2
    )


def chat_with_agent(user_message: str):
    llm = get_llm()
    
    # Prompt Engineering
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert AI Technical Project Manager. You help software development teams manage their Jira tasks, GitHub repositories, and overall workflow. Be highly professional, concise, and technical."),
        ("human", "{message}")
    ])
    
    # Build a LangChain Chain  (Prompt -> LLM -> Output Text)
    chain = prompt | llm | StrOutputParser()
    
    # Send User message and get an answer
    response = chain.invoke({"message": user_message})
    
    return response