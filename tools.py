def get_weather(city: str):
    # 先写死，后面可以接真实API
    return f"{city} 今天 25°C，晴天"

TOOLS = {
    "get_weather": get_weather
}