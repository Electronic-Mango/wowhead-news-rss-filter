# Wowhead news RSS filter

[Wowhead](https://www.wowhead.com/) does provide RSS feed for its [news](https://www.wowhead.com/news) section, however it's categories selection is limited.
For example - you cannot receive news only from live, there's only live+PTR.
You are also always receiving sponsored posts.

This REST API wraps Wowhead's RSS, but allows for filtering out any category you like.

The API is created with `Python3.11` and [`FastAPI`](https://fastapi.tiangolo.com/).



## Running the API

### Manually

1. Install all packages from `requirements.txt`
2. Start the api via `uvicorn`

```shell
pip install -r requirements.txt
uvicorn src.main:app
```

Uvicorn will by default start the API on address `127.0.0.1:8000`, you can change it via `--host <new host>` and `--port <new port>` parameters.
More details are in [Uvicorn documentation](https://www.uvicorn.org/settings/). 


### Docker

You can start the API via Docker Compose, without any additional configuration:
```shell
docker compose up -d --build
```

By default, Compose will forward local port 5021 to container port 8000, where the API is listening.
You can change both ports in `docker-compose.yml`, just make sure, that environment variable `UVICORN_PORT` matches new forwarded port on container side.

```yaml
environment:
  - UVICORN_PORT=8000
ports:
  - 5021:8000
```

You can remove `ports` section if you want to disable port forwarding.


## Endpoints

You can access (automatically generated) docs via `/`, `/docs` or `/redoc`.

Besides docs, there's only one endpoint `/news/{category}`.
You can check values for `category` at the bottom of [Wowhead news page](https://www.wowhead.com/news), there's a RSS button with all categories.
Just make sure that you check the last value in URL, not the name on the page.

Some examples (case sensitive) are:
 * [`all`](https://www.wowhead.com/news/rss/all)
 * [`retail`](https://www.wowhead.com/news/rss/retail)
 * [`diablo`](https://www.wowhead.com/news/rss/diablo)
 * [`classic-series`](https://www.wowhead.com/news/rss/classic-series)
 * [`other-blizzard-games`](https://www.wowhead.com/news/rss/other-blizzard-games)

Without any additional parameters it will just forward Wowhead news RSS for a given category.
You can remove articles from specific categories via `remove` query parameter.
You can specify multiple `remove` parameters to remove multiple different categories.

| Route                                                 | Description                                                             |
|-------------------------------------------------------|-------------------------------------------------------------------------|
| `/news/all`                                           | All unfiltered news                                                     |
| `/news/retail?remove=PTR`                             | Retail WoW news without articles from "PTR" category                    |
| `/news/classic-series?remove=Blizzard&remove=Wowhead` | Classic WoW news without articles from "Blizzard" or "Wowhead" category |
