import json
from llm import call_llm
from tools import TOOLS

SYSTEM_PROMPT = """
你是一个AI Agent，可以使用工具解决问题。

你必须使用以下JSON格式回答：

如果需要调用工具：
{
  "action": "tool",
  "tool_name": "工具名",
  "args": {参数}
}

如果直接回答：
{
  "action": "final",
  "answer": "你的回答"
}
"""

class Agent:
    def __init__(self, memory):
        self.memory = memory

    def run(self, user_input):
        self.memory.add("user", user_input)

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages += self.memory.get()

        response = call_llm(messages)

        try:
            result = json.loads(response)
        except:
            return "解析失败：" + response

        if result["action"] == "tool":
            tool_name = result["tool_name"]
            args = result["args"]

            if tool_name in TOOLS:
                tool_result = TOOLS[tool_name](**args)

                # 把工具结果再喂给模型
                self.memory.add("assistant", str(result))
                self.memory.add("tool", tool_result)

                return self.run("请根据工具结果给出最终答案")
            else:
                return f"未知工具：{tool_name}"

        elif result["action"] == "final":
            answer = result["answer"]
            self.memory.add("assistant", answer)
            return answer

        else:
            return "未知action"