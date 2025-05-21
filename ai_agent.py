# Setting up API Key for Groq and Tavily
import os 
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


# Setting up LLM
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

openai_llm = ChatOpenAI(model="gpt-4o-mini")
groq_llm = ChatGroq(model="llama-3.3-70b-versatile")


# Setting up AI agent with search tool functionality
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage


def get_response_from_agent(llm_id, query, allow_search, provider):
    
    if provider == "Groq":
        llm = ChatGroq(model = llm_id)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model = llm_id)

    role = "Act as an AI Travel Agent who is smart and friendly"
    search_tool = TavilySearchResults(max_results = 2) if allow_search else []

    agent = create_react_agent(
        model = llm,
        tools = search_tool,
        state_modifier = role
    )

    # Prompts
    state={"messages": query}
    response=agent.invoke(state)
    messages=response.get("messages")
    ai_messages=[message.content for message in messages if isinstance(message, AIMessage)]

    return ai_messages[-1]

