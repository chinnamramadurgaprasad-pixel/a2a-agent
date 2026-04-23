from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY missing")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

REGISTRY_URL = "http://127.0.0.1:8000/api/agents/register/"

@app.route('/')
def home():
    return {"message": "Summarizer Running"}

@app.route('/execute', methods=['POST'])
def execute():
    data = request.json
    task_id = data.get("task_id")
    text = data.get("input", {}).get("text", "")

    try:
        response = model.generate_content(f"Summarize:\n{text}")

        return jsonify({
            "task_id": task_id,
            "status": "success",
            "result": response.text,
            "error": None
        })

    except Exception as e:
        return jsonify({
            "task_id": task_id,
            "status": "error",
            "result": None,
            "error": str(e)
        })

def register():
    try:
        requests.post(REGISTRY_URL, json={
            "name": "Summarizer",
            "description": "AI summarizer",
            "capabilities": ["summarization"],
            "endpoint_url": "http://127.0.0.1:8002/execute"
        })
    except:
        print("Registry not available")

if __name__ == '__main__':
    register()
    app.run(port=8002)