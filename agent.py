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

        # 👉 Step 1：先做决策
        plan = self.planner.plan(user_input)

        action = plan["action"]
        args = plan.get("args", {})

        # 👉 Step 2：执行
        if action in TOOLS:
            try:
                result = TOOLS[action](**args)
            except Exception as e:
                result = str(e)

            # 👉 把工具结果写入上下文，再让 LLM 总结
            self.memory.add("system", f"工具 {action} 返回结果：\n{result}")
            return self.final_answer()

        elif action == "direct_answer":
            return self.final_answer()

        else:
            # planner 兜底：未知 action 直接走回答链路
            self.memory.add("system", f"planner 给出未知 action: {action}，已改为直接回答。")
            return self.final_answer()

    def final_answer(self):
        messages = self.memory.get()
        response = call_llm(messages)
        answer = response["choices"][0]["message"]["content"]

        self.memory.add("assistant", answer)
        return answer