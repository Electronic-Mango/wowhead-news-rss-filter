from typing import Annotated
from xml.etree.ElementTree import fromstring, tostring

from fastapi import FastAPI, Query
from requests import get

NEWS_RSS_URL = "https://www.wowhead.com/news&rss"

app = FastAPI(docs_url="/")


@app.get("/news")
async def news(remove: Annotated[list[str], Query()] = None):
    response = get(NEWS_RSS_URL).text
    if not remove:
        return response
    xml = fromstring(response)
    channel = xml.find("channel")
    for item in channel.findall("item"):
        if item.find("category").text in remove:
            channel.remove(item)
    return tostring(xml)
