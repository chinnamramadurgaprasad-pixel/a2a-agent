from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)

#  Load API key safely
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError(" GOOGLE_API_KEY missing in .env")

genai.configure(api_key=API_KEY)
#  Use supported model
model = genai.GenerativeModel("gemini-1.5-flash")

REGISTRY_URL = "http://127.0.0.1:8000/api/agents/register/"

# HOME ROUTE (for browser)
@app.route('/')
def home():
    return {
        "message": "Summarizer Agent Running",
        "usage": "POST /execute with JSON"
    }

# EXECUTE ROUTE
@app.route('/execute', methods=['GET', 'POST'])
def execute():

    #  Allow GET for testing
    if request.method == "GET":
        return {"message": "Use POST method with JSON body"}

    #  Safe JSON parsing
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "status": "error",
            "error": "Invalid or missing JSON body"
        }), 400

    task_id = data.get("task_id")
    text = data.get("input", {}).get("text", "")

    #  Validate input
    if not text.strip():
        return jsonify({
            "task_id": task_id,
            "status": "error",
            "result": None,
            "error": "Input text is empty"
        }), 400

    try:
        #  Better prompt
        prompt = f"Summarize the following text in a clear and concise way:\n\n{text}"

        response = model.generate_content(prompt)

        result_text = getattr(response, "text", None)

        if not result_text:
            raise Exception("Empty response from Gemini")

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
            "error": f"Gemini error: {str(e)}"
        })

# REGISTER AGENT
def register():
    try:
        res = requests.post(
            REGISTRY_URL,
            json={
                "name": "Summarizer",
                "description": "AI summarizer",
                "capabilities": ["summarization"],
                "endpoint_url": "http://127.0.0.1:8002/execute"
            },
            timeout=5
        )

        if res.status_code == 200:
            print(" Registered successfully")
        else:
            print(f" Registry error: {res.text}")

    except Exception as e:
        print(f" Registry not available: {e}")

# RUN APP
if __name__ == '__main__':
    register()
    app.run(port=8002)