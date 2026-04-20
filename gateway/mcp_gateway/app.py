from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute():
    query = request.json['input']['text']   # UPDATED

    result = f"Search results for: {query}"

    return jsonify({
        "task_id": request.json['task_id'],
        "status": "success",
        "result": result,
        "error": None
    })

def register():
    requests.post("http://localhost:8000/api/agents/register", json={
        "name": "Web Search Agent",
        "description": "Search via MCP",
        "capabilities": ["search"],
        "endpoint_url": "http://localhost:8003/execute"
    })

if __name__ == '__main__':
    register()
    app.run(port=8003)