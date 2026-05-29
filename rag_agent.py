from openai import OpenAI
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL, MAX_REACT_ROUNDS
from tools import TOOL_SCHEMAS, execute_tool

RAG_SYSTEM_PROMPT = """\
你是一个文档问答助手。用户会就文档内容提问，你需要先检索文档库再回答。

工作规则：
1. 收到用户问题后，先用 search_docs 工具在文档库中检索相关内容。
2. 基于检索到的文档片段回答用户问题，不要编造文档中没有的信息。
3. 如果检索结果不足以回答问题，如实告诉用户。
4. 回答时注明信息来源（文件名）。
5. 如果用户的问题和文档无关，直接回答即可。
"""

HYBRID_SYSTEM_PROMPT = """\
你是一个智能助手，可以同时查询文档库和 SQLite 数据库来回答用户问题。

工作规则：
1. 如果问题涉及文档知识，先用 search_docs 检索相关内容。
2. 如果问题涉及数据查询，先用 list_tables 了解表结构，再用 describe_table 查看详细结构，最后用 run_query 执行查询。
3. 可以结合文档和数据库的结果来综合回答。
4. 回答时注明信息来源。
"""


class RAGAgent:
    def __init__(self, mode: str = "rag"):
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
        )
        if mode == "hybrid":
            self.system_prompt = HYBRID_SYSTEM_PROMPT
        else:
            self.system_prompt = RAG_SYSTEM_PROMPT
        self.mode = mode

    def chat(self, question: str) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
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

            if not msg.tool_calls:
                return msg.content or "（模型未返回内容）"

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

            for tc in msg.tool_calls:
                import json
                args = json.loads(tc.function.arguments)
                result = execute_tool(tc.function.name, args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                })

        messages.append({
            "role": "user",
            "content": "请基于以上结果，用中文总结回答用户最初的问题。不要再调用工具。",
        })
        response = self.client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=messages,
        )
        return response.choices[0].message.content or "（模型未返回内容）"
