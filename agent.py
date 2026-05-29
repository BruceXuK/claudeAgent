from openai import OpenAI
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL, MAX_REACT_ROUNDS
from tools import TOOL_SCHEMAS, execute_tool

SYSTEM_PROMPT = """\
你是一个 SQL 查询助手。用户用自然语言提问，你需要通过查询 SQLite 数据库来回答。

工作规则：
1. 在写任何 SQL 查询之前，先用 list_tables 了解有哪些表，再用 describe_table 查看相关表的结构。
2. 查询结果用中文向用户解释，不要直接输出原始数据。
3. 如果查询出错，根据错误信息修正 SQL 后重试。
4. 只用 SELECT 语句，不要尝试修改数据。
5. 如果用户的问题和数据库无关，直接回答即可。
"""


class Agent:
    def __init__(self):
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
        )

    def chat(self, question: str) -> str:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ]

        for _ in range(MAX_REACT_ROUNDS):
            response = self.client.chat.completions.create(
                model=DEEPSEEK_MODEL,
                messages=messages,
                tools=TOOL_SCHEMAS,
                tool_choice="auto",
            )

            msg = response.choices[0].message

            # If model gives a final answer (no tool calls)
            if not msg.tool_calls:
                return msg.content or "（模型未返回内容）"

            # Append assistant message with tool calls
            messages.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in msg.tool_calls
                ],
            })

            # Execute each tool call and append results
            for tc in msg.tool_calls:
                import json
                args = json.loads(tc.function.arguments)
                result = execute_tool(tc.function.name, args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                })

        # Max rounds reached, ask model for final answer without tools
        messages.append({
            "role": "user",
            "content": "请基于以上查询结果，用中文总结回答用户最初的问题。不要再调用工具。",
        })
        response = self.client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=messages,
        )
        return response.choices[0].message.content or "（模型未返回内容）"
