from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)

# LOAD API KEY
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError(" GOOGLE_API_KEY missing in .env")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

REGISTRY_URL = "http://127.0.0.1:8000/api/agents/register/"

# HOME ROUTE (FOR TESTING)
@app.route('/')
def home():
    return {
        "message": "Math Agent Running",
        "usage": "POST /execute"
    }

# EXECUTE TASK
@app.route('/execute', methods=['GET', 'POST'])
def execute():

    # Prevent 405 error in browser
    if request.method == "GET":
        return jsonify({
            "message": "Use POST with JSON body",
            "example": {
                "task_id": "123",
                "input": {"text": "10 + 5"}
            }
        })

    #  Safe JSON parsing
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "error": "Invalid JSON input"
        }), 400

    task_id = data.get("task_id")
    input_text = data.get("input", {}).get("text")

    # Validate input
    if not input_text:
        return jsonify({
            "task_id": task_id,
            "status": "error",
            "result": None,
            "error": "Missing input.text"
        }), 400

    try:
        # GEMINI CALL
        response = model.generate_content(
            f"Solve this math problem step-by-step:\n{input_text}"
        )

        # Safe extraction
        result_text = getattr(response, "text", None)

        if not result_text:
            result_text = str(response)

        return jsonify({
            "task_id": task_id,
            "status": "success",
            "result": result_text,
            "error": None
        })

    except Exception as e:
        return jsonify({
            "task_id": task_id,
            "status": "error",
            "result": None,
            "error": str(e)
        })

# REGISTER AGENT
def register():
    try:
        res = requests.post(
            REGISTRY_URL,
            json={
                "name": "Math Helper",
                "description": "AI math solver",
                "capabilities": ["math"],
                "endpoint_url": "http://127.0.0.1:8001/execute"
            },
            timeout=5
        )

        print(" Registered:", res.status_code)

    except Exception as e:
        print(" Registry not available:", e)

# RUN APP
if __name__ == '__main__':
    register()
    app.run(port=8001, debug=True)