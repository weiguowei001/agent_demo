import json
from llm import call_llm
from tools import TOOLS
from planner import Planner
from prompts import SYSTEM_PROMPT

class Agent:
    def __init__(self, memory):
        self.memory = memory
        self.planner = Planner()
        self.memory.ensure_system_prompt(SYSTEM_PROMPT)

    def run(self, user_input):
        if not user_input.strip():
            return "请输入问题"
        self.memory.add("user", user_input)

        plan = self.planner.plan(user_input)

        steps = plan.get("steps", [])
        print("PLAN:", steps)

        context = ""

        # 👉 逐步执行
        for step in steps:
            action = step["action"]
            args = step.get("args", {})

            print("EXEC:", action, args)

            if action in TOOLS:
                try:
                    result = TOOLS[action](**args)
                except Exception as e:
                    result = str(e)

                # 👉 累积上下文
                context += f"\n[{action}结果]\n{result}\n"

        self.memory.add("system", f"以下是工具执行结果：\n{context}")
        # 👉 最终回答
        return self.final_answer()

    def final_answer(self):
        messages = self.memory.get()
        response = call_llm(messages)
        answer = response["choices"][0]["message"]["content"]

        self.memory.add("assistant", answer)
        return answer