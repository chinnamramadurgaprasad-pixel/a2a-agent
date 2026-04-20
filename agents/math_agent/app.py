from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

REGISTRY_URL = "http://localhost:8000/api/agents/register"

@app.route('/execute', methods=['POST'])
def execute():
    data = request.json
    task_id = data['task_id']

    input_text = data['input']['text']   # UPDATED

    try:
        result = str(eval(input_text))

        return jsonify({
            "task_id": task_id,
            "status": "success",
            "result": result,
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
    payload = {
        "name": "Math Helper",
        "description": "Solves math problems",
        "capabilities": ["math"],
        "endpoint_url": "http://localhost:8001/execute"
    }
    requests.post(REGISTRY_URL, json=payload)

if __name__ == '__main__':
    register()
    app.run(port=8001)