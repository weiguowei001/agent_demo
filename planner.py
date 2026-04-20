import json
from llm import call_llm
from prompts import PLANNER_PROMPT

class Planner:
    def plan(self, user_input):
        messages = [
            {"role": "system", "content": PLANNER_PROMPT},
            {"role": "user", "content": user_input}
        ]

        response = call_llm(messages)

        content = response["choices"][0]["message"]["content"]

        try:
            return json.loads(content)
        except:
            return {
                "action": "direct_answer",
                "args": {"query": user_input},
                "reason": "fallback"
            }
