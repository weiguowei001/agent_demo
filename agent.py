import json
from llm import call_llm
from tools import TOOLS
from prompts import REACT_PROMPT

class Agent:
    def __init__(self, memory):
        self.memory = memory

    def run(self, user_input):
        self.memory.add("user", user_input)

        messages = [
            {"role": "system", "content": REACT_PROMPT},
            {"role": "user", "content": user_input}
        ]

        for step in range(5):  # 最多5轮
            response = call_llm(messages)
            content = response["choices"][0]["message"]["content"]

            print(f"\n=== STEP {step} ===")
            print(content)

            # 👉 判断是否结束
            if "Final Answer:" in content:
                answer = content.split("Final Answer:")[-1].strip()
                self.memory.add("assistant", answer)
                return answer

            # 👉 解析 Action
            try:
                action_line = [line for line in content.split("\n") if "Action:" in line][0]
                input_line = [line for line in content.split("\n") if "Action Input:" in line][0]

                action = action_line.split("Action:")[1].strip()
                action_input = json.loads(input_line.split("Action Input:")[1].strip())

            except Exception as e:
                return f"解析失败: {e}\n{content}"

            # 👉 执行工具
            if action in TOOLS:
                try:
                    result = TOOLS[action](**action_input)
                except Exception as e:
                    result = str(e)
            else:
                result = f"未知工具: {action}"

            # 👉 把 Observation 加入上下文
            messages.append({
                "role": "assistant",
                "content": content
            })

            messages.append({
                "role": "user",
                "content": f"Observation: {result}"
            })

        return "超出最大推理步数"