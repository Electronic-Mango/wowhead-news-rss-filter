from http import HTTPStatus
from typing import Annotated
from xml.etree.ElementTree import fromstring, tostring

from fastapi import FastAPI, HTTPException, Query
from requests import get

NEWS_RSS_URL = "https://www.wowhead.com/news&rss"

app = FastAPI(docs_url="/")


@app.get("/news")
async def news(remove: Annotated[list[str], Query()] = None):
    response = get(NEWS_RSS_URL)
    if response.status_code != HTTPStatus.OK:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    if not remove:
        return response.text
    xml = fromstring(response.text)
    channel = xml.find("channel")
    for item in channel.findall("item"):
        if item.find("category").text in remove:
            channel.remove(item)
    return tostring(xml)
