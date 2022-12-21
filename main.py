from urllib.parse import unquote

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from helper.supported_sites import supported_sites

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/topnews")
async def call_api(
        site: str
):
    site = site.lower()
    if site in supported_sites.keys():
        resp = await supported_sites[site]["website"]().topnews()
        if resp is None:
            return {"error": "website blocked change ip or domain"}
        elif len(resp["data"]) > 0:
            return resp
        else:
            return {"error": "no results found"}
    return {"error": "invalid site"}


@app.get("/api/readmore")
async def call_api(
        site: str, url: str
):
    site = site.lower()
    url = unquote(url)
    if site in supported_sites.keys():
        resp = await supported_sites[site]["website"]().readmore(url)
        if resp is None:
            return {"error": "website blocked change ip or domain"}
        elif len(resp["post"]) > 0:
            return resp
        else:
            return {"error": "no results found"}
    return {"error": "invalid site"}


@app.get("/")
async def home():
    sites_list = [
        site
        for site in supported_sites.keys()
    ]
    return {"info": "LK-NewsApi", "supported-sites": sites_list}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
