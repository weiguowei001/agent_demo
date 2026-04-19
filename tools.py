import requests
from bs4 import BeautifulSoup


def search_web(query: str):
    url = "https://duckduckgo.com/html/"
    params = {"q": query}

    response = requests.post(url, data=params)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for a in soup.select(".result__a")[:5]:
        title = a.get_text()
        link = a.get("href")
        results.append(f"{title} - {link}")

    return "\n".join(results)

def fetch_webpage(url: str):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")

        # 去掉script/style
        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        return text[:2000]  # 防止太长
    except Exception as e:
        return f"网页读取失败: {str(e)}"

def get_weather(city: str):
    return f"{city} 当前天气：25°C，晴"

from rag import RAG

rag = RAG("../speak_with_chatgpt")  # 你的代码/文档目录

def rag_search(query: str):
    result = rag.search(query)
    return result[:2000]  # 限制长度

TOOLS = {
    "search_web": search_web,
    "fetch_webpage": fetch_webpage,
    "get_weather": get_weather,
    "rag_search" : rag_search,
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "搜索互联网信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_webpage",
            "description": "获取网页内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string"}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "rag_search",
            "description": "从本地知识库/代码库检索。当问题与项目文件、源码、实现方式相关时应优先使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    }
]
