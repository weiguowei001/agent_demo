from agent import Agent
from memory import Memory

def main():
    memory = Memory()
    agent = Agent(memory)

    print("AI Agent 启动，输入 exit 退出")

    while True:
        user_input = input(">>> ")

        if user_input == "exit":
            break

        result = agent.run(user_input)
        print("Agent:", result)


if __name__ == "__main__":
    main()