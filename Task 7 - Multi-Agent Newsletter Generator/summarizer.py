from pydantic import BaseModel
from typing import List
import re
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
import tenacity
from config import config

class ArticleSummary(BaseModel):
    title: str
    url: str
    source: str
    summary: str

def clean_summary(text):
    text = re.sub(
        r"^(here (is|are)|here's|this (is|was)|according to (the )?article|in this article)[\s:,-]*", 
        "", 
        text.strip(), 
        flags=re.IGNORECASE
    )
    return text.strip()

@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
    retry=tenacity.retry_if_exception_type(Exception),
)
def summarize_article(article, model="llama3:8b"):
    prompt_template = PromptTemplate.from_template(
        "Summarize this Web3 news article in 2-3 sentences for a newsletter.\n"
        "Title: {title}\n"
        "Source: {source}\n"
    )
    
    llm = OllamaLLM(model=model)
    prompt = prompt_template.format(
        title=article['title'],
        source=article['source']
    )
    
    summary = llm.invoke(prompt)
    return ArticleSummary(
        title=article['title'],
        url=article['url'],
        source=article['source'],
        summary=clean_summary(summary),
    )

def summarize_articles(articles: List[dict]) -> List[ArticleSummary]:
    return [summarize_article(a) for a in articles]