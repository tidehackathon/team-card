from pydantic import BaseModel

class Article(BaseModel):
    article_text: str