# Setting up Pydantic model
from pydantic import BaseModel
from typing import List

class RequestState(BaseModel):
    model_name: str
    model_provider: str
    messages: List[str]
    allow_search: bool

# Setting up AI Agent from Frontend Request
from fastapi import FastAPI
from ai_agent import get_response_from_agent

ALLOWED_MODEL_NAMES = {"gpt-4o-mini", "llama-3.3-70b-versatile"}

app = FastAPI(title="Travel AI agent")

@app.post("/chat")
def chat_endpoint(request: RequestState):

    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "This AI model is invalid."}
    
    # Get response from AI agent

    llm_id = request.model_name
    query = request.messages
    allow_search = request.allow_search
    provider = request.model_provider
    
    response = get_response_from_agent(llm_id, query, allow_search, provider)

    return response
    

# Run App
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8080)
    