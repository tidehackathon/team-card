from fastapi import FastAPI
import numpy as np
import json
from classes import Article
from predict import predictor, get_explanation

app = FastAPI()

@app.get("/")
async def root():
    return {"info": "This is a disinformation detection model API"}

@app.post("/check_fake/")
async def check_fraud(items: Article):
    data = json.loads(items.json())
    prob = predictor(data['article_text'])
    return {"result": bool(not(np.argmax(prob)))}

