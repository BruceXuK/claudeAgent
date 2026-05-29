import sys
from config import DOCS_DIR
from rag_loader import load_docs
from rag_store import index_chunks, reset_store


def main():
    reset = "--reset" in sys.argv
    if reset:
        print("清空向量数据库...")
        reset_store()

    print(f"扫描文档目录: {DOCS_DIR}")
    chunks = load_docs(DOCS_DIR)
    if not chunks:
        print("未找到文档。请将 PDF/Markdown/TXT 文件放入 docs/ 目录。")
        return

    print(f"共 {len(chunks)} 个文本块，正在生成向量并存储...")
    index_chunks(chunks)
    print("索引完成。")


if __name__ == "__main__":
    main()
