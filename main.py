from fastapi import FastAPI
from requests import get

NEWS_RSS_URL = "https://www.wowhead.com/news&rss"

app = FastAPI()


@app.get("/")
async def root():
    return "Wowhead news RSS filter"


@app.get("/news")
async def news():
    response = get(NEWS_RSS_URL)
    return response.text
