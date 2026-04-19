def get_weather(city: str):
    # 先写死，后面可以接真实API
    return f"{city} 今天 25°C，晴天"

TOOLS = {
    "get_weather": get_weather
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取城市天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名"
                    }
                },
                "required": ["city"]
            }
        }
    }
]