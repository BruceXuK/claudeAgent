# AI 智能体平台

基于 DeepSeek API 的 ReAct Agent，支持两种模式：

- **SQL 问答** — 用自然语言查询 SQLite 数据库
- **RAG 文档问答** — 在本地文档中检索并回答问题
- **混合模式** — 同时查询文档和数据库

## 快速开始

```bash
export DEEPSEEK_API_KEY="sk-xxx"
pip install -r requirements.txt

# SQL 问答
python main.py

# RAG 文档问答（需先索引文档）
python main.py --index
python main.py --mode rag

# 混合模式（文档 + SQL）
python main.py --mode hybrid
```

## 工作原理

```
用户提问 → ReAct 循环 → 回答

ReAct 循环（最多 8 轮）：
  1. 发送消息给 DeepSeek
  2. 模型决定：调用工具 OR 给出回答
  3. 若调用工具 → 执行 → 结果反馈 → 回到步骤 1
  4. 若给出回答 → 输出给用户
```

## 三种模式

| 模式 | 命令 | 可用工具 |
|------|------|---------|
| SQL 问答 | `python main.py` | `list_tables`, `describe_table`, `run_query` |
| 文档问答 | `python main.py --mode rag` | `search_docs` |
| 混合模式 | `python main.py --mode hybrid` | 以上全部 |

## 工具

| 工具 | 功能 |
|------|------|
| `list_tables` | 列出所有表名 |
| `describe_table` | 查看表结构 |
| `run_query` | 执行 SELECT 查询（只读） |
| `search_docs` | 在文档库中检索相关内容 |

## RAG 索引

将 PDF、Markdown、TXT 文件放入 `docs/` 目录，然后索引：

```bash
python main.py --index        # 增量索引
python main.py --index --reset # 清空重建
```

## 技术栈

| 组件 | 技术 |
|------|------|
| LLM | DeepSeek（deepseek-chat） |
| 嵌入模型 | all-MiniLM-L6-v2（本地） |
| 向量数据库 | Chroma |
| SQL 数据库 | SQLite |
| 文档解析 | PyPDF2 |
