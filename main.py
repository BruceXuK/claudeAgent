import sys
import os
from db import init_db
from agent import Agent
from rag_agent import RAGAgent
from config import DEEPSEEK_API_KEY


def print_usage():
    print("用法:")
    print("  python main.py              # 默认 SQL 问答模式")
    print("  python main.py --mode rag   # 文档问答模式")
    print("  python main.py --mode hybrid # 混合模式（文档 + SQL）")
    print("  python main.py --index      # 索引文档后退出")


def main():
    if "--index" in sys.argv:
        from config import DOCS_DIR
        if not os.path.isdir(DOCS_DIR):
            print(f"文档目录不存在: {DOCS_DIR}")
            return
        from index_docs import main as index_main
        index_main()
        return

    mode = "sql"
    for i, arg in enumerate(sys.argv):
        if arg == "--mode" and i + 1 < len(sys.argv):
            mode = sys.argv[i + 1]
            break

    if mode not in ("sql", "rag", "hybrid"):
        print(f"未知模式: {mode}")
        print_usage()
        return

    if mode in ("rag", "hybrid"):
        from config import DOCS_DIR
        if not os.path.isdir(DOCS_DIR):
            os.makedirs(DOCS_DIR, exist_ok=True)
        from rag_store import _get_collection
        try:
            _get_collection()
        except Exception:
            print("提示：尚未索引文档。请先运行:")
            print("  python main.py --index")
            print()

    if not DEEPSEEK_API_KEY:
        print("错误：请设置环境变量 DEEPSEEK_API_KEY")
        print("  export DEEPSEEK_API_KEY='sk-xxx'")
        return

    print("初始化数据库...")
    init_db()

    if mode == "sql":
        print("初始化 SQL 智能体...")
        agent = Agent()
    else:
        label = "文档问答" if mode == "rag" else "混合模式"
        print(f"初始化 {label} 智能体...")
        agent = RAGAgent(mode=mode)

    mode_labels = {"sql": "SQL 问答", "rag": "文档问答", "hybrid": "混合模式"}
    print(f"\n{mode_labels[mode]}智能体已就绪！输入问题，输入 /exit 退出。\n")

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

        print()
        answer = agent.chat(question)
        print(answer)
        print()


if __name__ == "__main__":
    main()
