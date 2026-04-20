from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

REGISTRY_URL = "http://localhost:8000/api/agents/register"

@app.route('/execute', methods=['POST'])
def execute():
    data = request.json

    text = data['input']['text']   # UPDATED

    summary = text[:100]

    return jsonify({
        "task_id": data['task_id'],
        "status": "success",
        "result": summary,
        "error": None
    })

def register():
    payload = {
        "name": "Summarizer",
        "description": "Summarizes text",
        "capabilities": ["summarization"],
        "endpoint_url": "http://localhost:8002/execute"
    }
    requests.post(REGISTRY_URL, json=payload)

if __name__ == '__main__':
    register()
    app.run(port=8002)