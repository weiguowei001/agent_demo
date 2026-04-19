import os
import requests

BASE_URL = "https://api.deepseek.com/v1/chat/completions"

def call_llm(messages, tools=None):
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.7
    }

    if tools:
        data["tools"] = tools
        data["tool_choice"] = "auto"

    response = requests.post(BASE_URL, headers=headers, json=data)
    return response.json()