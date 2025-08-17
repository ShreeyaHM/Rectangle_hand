import requests

def get_poem():
    API_KEY = "API_KEY"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

    prompt = "write a poem on love like connect it with elements of nature"

    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    return result["candidates"][0]["content"]["parts"][0]["text"]
