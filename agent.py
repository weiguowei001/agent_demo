import json
from llm import call_llm
from tools import TOOLS, TOOL_SCHEMAS

class Agent:
    def __init__(self, memory):
        self.memory = memory

    def run(self, user_input):
        self.memory.add("user", user_input)

        messages = self.memory.get()

        response = call_llm(messages, tools=TOOL_SCHEMAS)
        msg = response["choices"][0]["message"]

        # 👉 关键：是否触发 tool_calls
        if "tool_calls" in msg:
            self.memory.add("assistant", msg)

            for tool_call in msg["tool_calls"]:
                tool_name = tool_call["function"]["name"]
                args = json.loads(tool_call["function"]["arguments"])
                tool_call_id = tool_call["id"]

                if tool_name in TOOLS:
                    result = TOOLS[tool_name](**args)

                    # 👉 关键：带 tool_call_id 回传
                    self.memory.add("tool", {
                        "tool_call_id": tool_call_id,
                        "content": result
                    })

                else:
                    self.memory.add("tool", {
                        "tool_call_id": tool_call_id,
                        "content": f"未知工具 {tool_name}"
                    })

            # 再让模型生成最终答案
            return self.run("")

        else:
            content = msg["content"]
            self.memory.add("assistant", content)
            return content