import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import os

app = FastAPI(
    title='An ai powered docker app',
    description='A local llm powered by Ollama running inside docker',
    version='1.0.0'
)

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434/api/generate')
MODEL_NAME = os.getenv('MODEL_NAME', 'llama3.2:1b')

# Request and Response models

class AskRequest(BaseModel):
    question:str

class AskResponse(BaseModel):
    question:str
    answer:str
    model:str

#health check endpoint

@app.get('/')
async def health_check():
    return {
        "status": 'ok',
        'message': 'Docker ai app is running',
        'model': MODEL_NAME
    }

@app.post('/ask', response_model=AskResponse)
async def ask(request: AskRequest):
    
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail='Question cannot be empty'
        )
    payload = {
        'model': MODEL_NAME,
        'prompt': request.question,
        'stream' : False
    }
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            
        data = response.json()
        answer = data.get('response', '').strip()
        
        if not answer:
            raise HTTPException(status_code=500, detail='Model returned an empty response')
        
        return AskResponse(
            question = request.question,
            answer= answer,
            model= MODEL_NAME
        )
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail='Cannot connect to Ollama. Make sure it is running on port 11434.')
    
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail='Ollama took too long to respond. Try shorter question.')
    
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail= f'Ollama returned an error {e.response.status_code}.')
    
    
        



