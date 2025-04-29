
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


@app.get("/trending", response_class=JSONResponse)
async def trending():
    try:
        api = api_manager.get_api()
        res = requests.get(api.rstrip('/') + '/api/v1/trending', timeout=10)
        return res.json()
    except Exception as e:
        print(f"[trending] エラー: {e}")
        return JSONResponse(content={"error": "トレンド取得に失敗しました"}, status_code=500)


@app.get("/search", response_class=JSONResponse)
async def search(q: str, page: int = 1):
    results = []
    try:
        api = api_manager.get_api()
        search_url = f"{api.rstrip('/')}/api/v1/search?q={urllib.parse.quote(q)}&page={page}&hl=ja"
        res = requests.get(search_url, timeout=10)
        if res.ok:
            results += res.json()
    except Exception as e:
        print(f"[search] Invidious検索失敗: {e}")

    # Googleサジェスト追加
    try:
        suggest_url = f"http://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q={urllib.parse.quote(q)}"
        res2 = requests.get(suggest_url, timeout=10)
        if res2.ok:
            suggestions = res2.json()[1]
            for s in suggestions:
                results.append({"type": "suggestion", "title": s})
    except Exception as e:
        print(f"[search] Googleサジェスト失敗: {e}")

    return results


@app.get("/watch", response_class=JSONResponse)
async def watch(v: str):
    try:
        api = api_manager.get_api()
        video_url = f"{api.rstrip('/')}/api/v1/videos/{urllib.parse.quote(v)}"
        res = requests.get(video_url, timeout=10)
        return res.json()
    except Exception as e:
        print(f"[watch] エラー: {e}")
        return JSONResponse(content={"error": "動画情報取得に失敗しました"}, status_code=500)


@app.get("/channel", response_class=JSONResponse)
async def channel(c: str):
    try:
        api = api_manager.get_api()
        channel_url = f"{api.rstrip('/')}/api/v1/channels/{urllib.parse.quote(c)}"
        res = requests.get(channel_url, timeout=10)
        return res.json()
    except Exception as e:
        print(f"[channel] エラー: {e}")
        return JSONResponse(content={"error": "チャンネル情報取得に失敗しました"}, status_code=500)


@app.get("/playlist", response_class=JSONResponse)
async def playlist(p: str, page: int = 1):
    try:
        api = api_manager.get_api()
        playlist_url = f"{api.rstrip('/')}/api/v1/playlists/{urllib.parse.quote(p)}?page={page}"
        res = requests.get(playlist_url, timeout=10)
        return res.json()
    except Exception as e:
        print(f"[playlist] エラー: {e}")
        return JSONResponse(content={"error": "プレイリスト情報取得に失敗しました"}, status_code=500)
