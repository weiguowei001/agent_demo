from pathlib import Path

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

rag = RAG("./data")  # 你的代码/文档目录

def rag_search(query: str):
    result = rag.search(query)
    return result[:2000]  # 限制长度


def save_document(filename: str, content: str) -> str:
    """将文本保存到项目内 data/exports（禁止写出该目录之外）。"""
    root = (Path(__file__).resolve().parent / "data" / "exports").resolve()
    root.mkdir(parents=True, exist_ok=True)
    target = (root / filename).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        return "保存失败：路径必须在项目目录 data/exports 下"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"已保存到 {target}"


TOOLS = {
    "search_web": search_web,
    "fetch_webpage": fetch_webpage,
    "get_weather": get_weather,
    "rag_search": rag_search,
    "save_document": save_document,
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
            "description": "从本地知识库检索。当问题与教你说话时应优先使用。",
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
            "name": "save_document",
            "description": "将文本内容保存为本地文档（UTF-8）。文件会写入项目下的 data/exports 目录，文件名可带子路径如 notes/备忘.txt。",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "相对路径文件名，例如 report.md 或 subdir/out.txt",
                    },
                    "content": {
                        "type": "string",
                        "description": "要写入文件的完整文本",
                    },
                },
                "required": ["filename", "content"],
            },
        },
    },
]
