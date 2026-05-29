from db import init_db
from agent import Agent
from config import DEEPSEEK_API_KEY


def main():
    if not DEEPSEEK_API_KEY:
        print("错误：请设置环境变量 DEEPSEEK_API_KEY")
        print("  export DEEPSEEK_API_KEY='sk-xxx'")
        return

    print("初始化数据库...")
    init_db()

    print("初始化 DeepSeek 智能体...")
    agent = Agent()

    print("\nSQL 问答智能体已就绪！输入你的问题，输入 /exit 退出。\n")

    while True:
        try:
            question = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not question:
            continue
        if question == "/exit":
            print("再见！")
            break

        print()  # blank line before answer
        answer = agent.chat(question)
        print(answer)
        print()  # blank line after answer


if __name__ == "__main__":
    main()
