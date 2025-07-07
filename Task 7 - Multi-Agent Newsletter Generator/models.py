from pydantic import BaseModel, HttpUrl

class Article(BaseModel):
    title: str
    url: HttpUrl
    source: str

class ArticleSummary(BaseModel):
    title: str
    url: HttpUrl
    source: str
    summary: str