
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api_manager import APIManager
import requests
import urllib.parse

app = FastAPI()
api_manager = APIManager()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/watch", response_class=HTMLResponse)
async def watch(request: Request, v: str = ""):
    if not v:
        return RedirectResponse(url="/")  # video IDないときはトップへ
    return templates.TemplateResponse("watch.html", {"request": request, "video_id": v})

@app.get("/channel", response_class=HTMLResponse)
async def channel(request: Request, c: str = ""):
    if not c:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("channel.html", {"request": request, "channel_id": c})

@app.get("/searchpage", response_class=HTMLResponse)
async def searchpage(request: Request, q: str = ""):
    return templates.TemplateResponse("search.html", {"request": request, "query": q})

@app.get("/playlist", response_class=HTMLResponse)
async def playlist(request: Request, p: str = ""):
    if not p:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("playlist.html", {"request": request, "playlist_id": p})

@app.get("/trendingpage", response_class=HTMLResponse)
async def trendingpage(request: Request):
    return templates.TemplateResponse("trending.html", {"request": request})
