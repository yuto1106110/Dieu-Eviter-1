# Dieu Eviter: Flask-based Invidious Proxy + yt-dlp backend

from flask import Flask, request, jsonify
import requests
import subprocess
import json
import random

app = Flask(__name__)

# 使用するInvidiousインスタンス一覧
INVIDIOUS_INSTANCES = [
    "https://yewtu.be",
    "https://vid.puffyan.us",
    "https://inv.tux.pizza",
    "https://invidious.slipfox.xyz"
]

def get_fastest_instance(endpoint="/api/v1/trending"):
    results = []
    for instance in INVIDIOUS_INSTANCES:
        try:
            r = requests.get(instance + endpoint, timeout=2)
            if r.status_code == 200:
                results.append((instance, r.elapsed.total_seconds()))
        except:
            continue
    if results:
        return sorted(results, key=lambda x: x[1])[0][0]
    return random.choice(INVIDIOUS_INSTANCES)

@app.route("/api/search")
def search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing search query"}), 400
    instance = get_fastest_instance()
    try:
        res = requests.get(f"{instance}/api/v1/search", params={"q": query})
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": "API failed", "detail": str(e)}), 500

@app.route("/api/video")
def get_video():
    video_id = request.args.get("id")
    if not video_id:
        return jsonify({"error": "Missing video ID"}), 400
    instance = get_fastest_instance()
    try:
        res = requests.get(f"{instance}/api/v1/videos/{video_id}")
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": "API failed", "detail": str(e)}), 500

@app.route("/api/channel")
def get_channel():
    channel_id = request.args.get("id")
    if not channel_id:
        return jsonify({"error": "Missing channel ID"}), 400
    instance = get_fastest_instance()
    try:
        res = requests.get(f"{instance}/api/v1/channels/{channel_id}")
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": "API failed", "detail": str(e)}), 500

@app.route("/api/stream")
def get_stream():
    video_id = request.args.get("id")
    if not video_id:
        return jsonify({"error": "Missing video ID"}), 400
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        result = subprocess.run(["yt-dlp", "-f", "bestaudio", "-j", url], capture_output=True, text=True)
        info = json.loads(result.stdout)
        return jsonify({
            "url": info["url"],
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail")
        })
    except Exception as e:
        return jsonify({"error": "yt-dlp failed", "detail": str(e)}), 500

@app.route("/api/trending")
def trending():
    instance = get_fastest_instance()
    try:
        res = requests.get(f"{instance}/api/v1/trending")
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": "API failed", "detail": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
