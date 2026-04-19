class Memory:
    def __init__(self):
        self.history = []

    def add(self, role, content):
        if role == "tool":
            body = content["content"]
            if not isinstance(body, str):
                body = str(body)
            self.history.append({
                "role": "tool",
                "tool_call_id": content["tool_call_id"],
                "content": body,
            })
        elif role == "assistant" and isinstance(content, dict) and content.get("tool_calls"):
            # OpenAI/DeepSeek：assistant 含 tool_calls 时 content 必须是字符串（可为空），不能嵌套整条 message
            text = content.get("content")
            self.history.append({
                "role": "assistant",
                "content": text if isinstance(text, str) else ("" if text is None else str(text)),
                "tool_calls": content["tool_calls"],
            })
        else:
            self.history.append({
                "role": role,
                "content": content
            })

    def get(self):
        return self.history[-10:]