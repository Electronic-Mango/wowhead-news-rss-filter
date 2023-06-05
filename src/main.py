from http import HTTPStatus
from typing import Annotated
from xml.etree.ElementTree import fromstring, tostring

from fastapi import FastAPI, HTTPException, Query
from requests import Response, get

NEWS_RSS_URL = "https://www.wowhead.com/news/rss/{category}"

app = FastAPI(docs_url="/")


@app.get("/news/{category}")
async def news(category: str, remove: Annotated[list[str], Query()] = None):
    response = get(NEWS_RSS_URL.format(category=category))
    verify_response(response)
    return filter_results(response.text, remove) if remove else response.text


def verify_response(response: Response):
    if response.status_code != HTTPStatus.OK:
        raise HTTPException(status_code=response.status_code, detail=response.text)


def filter_results(response: str, remove: list[str]):
    xml = fromstring(response)
    channel = xml.find("channel")
    for item in channel.findall("item"):
        if item.find("category").text in remove:
            channel.remove(item)
    return tostring(xml)
