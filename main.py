import os
import requests
from fastapi import FastAPI, File, UploadFile, Body, Query, HTTPException
import base64
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Annotated
from pydantic import Field

load_dotenv()
app = FastAPI()
class ChatMessage(BaseModel):
   role: str
   content: str
class ChatHistory(BaseModel):
   data: list[ChatMessage]
client = OpenAI(base_url=os.environ.get("OPENAI_BASE_URL"),
               api_key=os.environ.get("OPENAI_API_KEY"))

@app.post("/chat/upload")
async def create_upload_file(file: UploadFile = File(...)):
   contents = await file.read()
   encoded_string = base64.b64encode(contents).decode('utf-8')
   image_url = f"data:image/png;base64,{encoded_string}"
   response = client.beta.chat.completions.parse(
     model="gpt-4o-mini-2024-07-18",
    #  model="gpt-4o",
     messages=[
       {
         "role": "user",
         "content": [
           {"type": "text", "text": """请帮助我提取这张图片中的聊天记录，请注意，绿色的部分为用户自己(role为user)，而白色的部分则为聊天对象(role 为顶部显示的名称)。"""},
           {
             "type": "image_url",
             "image_url": {
               "url": image_url,
             },
           },
         ],
       }
     ],
     response_format=ChatHistory
   )
   return [{"role": x.role, "content": x.content} for x in response.choices[0].message.parsed.data]

@app.get("/chat/image")
async def create_upload_file(image_url: Annotated[str, Query(...)]):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  
        
        contents = response.content
        encoded_string = base64.b64encode(contents).decode('utf-8')
        image_url_base64 = f"data:image/png;base64,{encoded_string}"
        
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": """请帮助我提取这张图片中的聊天记录，请注意，绿色的部分为用户自己(role为user)，而白色的部分则为聊天对象(role 为顶部显示的名称)。"""},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url_base64,
                            },
                        },
                    ],
                }
            ],
            response_format=ChatHistory
        )
        
        return [{"role": x.role, "content": x.content} for x in response.choices[0].message.parsed.data]
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch image from URL: {str(e)}")
