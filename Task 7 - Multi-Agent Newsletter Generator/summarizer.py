from pydantic import BaseModel
from typing import List
import re

# Use the updated LangChain Ollama integration
try:
    from langchain_ollama import OllamaLLM
    use_new_ollama = True
except ImportError:
    from langchain_community.llms.ollama import Ollama
    use_new_ollama = False

from langchain.prompts import PromptTemplate

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
    text = re.sub(r"^summary[\s:,-]*", "", text.strip(), flags=re.IGNORECASE)
    return text.strip()

def summarize_article(article, model="llama3:8b"):
    prompt_template = PromptTemplate.from_template(
        "Summarize the following Web3 news article in 2-3 sentences for a newsletter. "
        "Your response should be only the summary itself, without any introductory phrases.\n"
        "Title: {title}\n"
        "URL: {url}\n"
        "Source: {source}\n"
    )
    try:
        if use_new_ollama:
            llm = OllamaLLM(model=model)
        else:
            llm = Ollama(model=model)
        prompt = prompt_template.format(
            title=article['title'],
            url=article['url'],
            source=article['source']
        )
        summary = llm.invoke(prompt)
        summary = clean_summary(summary)
    except Exception as e:
        print(f"LangChain Ollama error: {e}")
        summary = "Summary unavailable due to local LLM error."
    return ArticleSummary(
        title=article['title'],
        url=article['url'],
        source=article['source'],
        summary=summary,
    )

def summarize_articles(articles: List[dict], model="llama3:8b") -> List[ArticleSummary]:
    return [summarize_article(a, model=model) for a in articles]