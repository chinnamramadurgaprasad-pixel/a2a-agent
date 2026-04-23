from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
    raise ValueError("Missing API keys")

@app.route('/')
def home():
    return {
        "message": "Search Agent Running",
        "endpoint": "/execute (POST)"
    }

@app.route('/execute', methods=['GET', 'POST'])
def execute():

    if request.method == "GET":
        return {"message": "Use POST method"}

    data = request.json
    task_id = data.get("task_id")
    query = data.get("input", {}).get("text", "")

    try:
        results = google_search(query)

        return jsonify({
            "task_id": task_id,
            "status": "success",
            "result": results,
            "error": None
        })

    except Exception as e:
        return jsonify({
            "task_id": task_id,
            "status": "error",
            "result": None,
            "error": str(e)
        })


def google_search(query):
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": query
    }

    res = requests.get(url, params=params, timeout=5)

    if res.status_code != 200:
        raise Exception(res.text)

    data = res.json()

    return [
        {
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet")
        }
        for item in data.get("items", [])[:5]
    ]

if __name__ == '__main__':
    app.run(port=8003)