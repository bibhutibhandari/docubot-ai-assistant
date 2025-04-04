from fastapi import FastAPI, HTTPException
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langserve import add_routes
from langchain.schema import HumanMessage
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import uvicorn



load_dotenv()
openai_api_key= os.getenv("OPENAI_API_KEY")
print(openai_api_key)

app = FastAPI()

model = ChatOpenAI(

    openai_api_key = openai_api_key,
    model_name = "gpt-3.5-turbo",
    temperature = 0.7
)

class TextRequest(BaseModel):
    prompt: str
    max_tokens: int = 100


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/generate")
async def generate_text(request: TextRequest):
    try:
        print(request.prompt)

        message = HumanMessage(content = request.prompt)

        response = model([message], max_tokens = request.max_tokens)

        return{

            "response" : response.content,
            "prompt" : request.prompt
        }


    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))

@app.get("/test")
async def test_app():
    return{"status":"good"}

