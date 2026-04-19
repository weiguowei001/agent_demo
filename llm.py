import requests

API_KEY = ""
BASE_URL = "https://api.deepseek.com/v1/chat/completions"

def call_llm(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post(BASE_URL, headers=headers, json=data)
    result = response.json()
    print(result)
    return result["choices"][0]["message"]["content"]