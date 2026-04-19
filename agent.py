import json
from llm import call_llm
from prompts import SYSTEM_PROMPT
from tools import TOOLS, TOOL_SCHEMAS


class Agent:
    def __init__(self, memory):
        self.memory = memory
        self.memory.ensure_system_prompt(SYSTEM_PROMPT)

    def run(self, user_input):
        self.memory.add("user", user_input)

        while True:
            messages = self.memory.get()
            response = call_llm(messages, tools=TOOL_SCHEMAS)
            msg = response["choices"][0]["message"]
            print(msg)
            # 👉 如果模型要调用工具
            if "tool_calls" in msg:
                self.memory.add("assistant", msg)

                for tool_call in msg["tool_calls"]:
                    tool_name = tool_call["function"]["name"]
                    args = json.loads(tool_call["function"]["arguments"])
                    tool_call_id = tool_call["id"]

                    if tool_name in TOOLS:
                        result = TOOLS[tool_name](**args)
                    else:
                        result = f"未知工具: {tool_name}"

                    self.memory.add("tool", {
                        "tool_call_id": tool_call_id,
                        "content": result
                    })

            else:
                # 👉 最终回答
                content = msg["content"]
                self.memory.add("assistant", content)
                return content