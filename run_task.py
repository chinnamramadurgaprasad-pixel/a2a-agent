import requests

data = {
    "capability": "math",
    "input": "100 + 200"
}

res = requests.post("http://localhost:8000/api/orchestrate/", json=data)
print(res.json())