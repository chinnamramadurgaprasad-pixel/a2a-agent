import requests
from django.conf import settings

def google_search(query):
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": settings.GOOGLE_API_KEY,
        "cx": settings.GOOGLE_CSE_ID,
        "q": query
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {"error": response.text}

    data = response.json()

    results = []
    for item in data.get("items", [])[:3]:
        results.append({
            "title": item["title"],
            "link": item["link"],
            "snippet": item["snippet"]
        })

    return results