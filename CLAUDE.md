# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 运行

```bash
export DEEPSEEK_API_KEY="sk-xxx"
pip install -r requirements.txt
python main.py
```

## 架构

```
main.py          # CLI 入口，交互式对话
agent.py         # ReAct 循环：LLM 决策 → 工具调用 → 结果反馈 → 回答（最多 8 轮）
tools.py         # 3 个工具：list_tables / describe_table / run_query（仅允许 SELECT）
db.py            # SQLite 连接 + 电商示例数据初始化
config.py        # DeepSeek API 配置（base_url、model、api_key）
requirements.txt # openai SDK
```

- **ReAct 循环**（agent.py）：每轮将消息发送给 DeepSeek，模型返回 `tool_calls` 或最终回答。工具执行结果以 `role: "tool"` 回传。超轮次后强制要求模型总结。
- **工具调用**（tools.py）：OpenAI 兼容的 function calling schema，DeepSeek 原生支持 `tool_choice: "auto"`。
- **安全约束**：`run_query` 仅接受 SELECT/WITH/EXPLAIN/PRAGMA 开头的语句，写操作在代码层拦截。
- **数据库**：SQLite，首次运行自动创建 `ecommerce.db` 并播种 users/products/orders 三张表。
