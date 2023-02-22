from fastapi import FastAPI
import json
from classes import Message
from model import get_top_similar

app = FastAPI()

@app.get("/")
async def root():
    return {"info": "This is a disinformation detection text matching model API"}

@app.post("/match_fake/")
async def check_fraud(items: Message):
    data = json.loads(items.json())
    similar_stories = get_top_similar(data['message_text'], thresh=0.88)
    return similar_stories
