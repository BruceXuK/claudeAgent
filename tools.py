import json
from db import get_connection
from rag_store import search as search_docs_fn

# OpenAI-compatible tool schemas for DeepSeek
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "list_tables",
            "description": "列出数据库中所有的表名",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "describe_table",
            "description": "获取指定表的完整结构（CREATE TABLE 语句）",
            "parameters": {
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "要描述的表名",
                    }
                },
                "required": ["table_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_query",
            "description": "执行只读 SQL 查询（仅支持 SELECT），返回查询结果",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql": {
                        "type": "string",
                        "description": "要执行的 SQL 查询语句，必须是 SELECT 语句",
                    }
                },
                "required": ["sql"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_docs",
            "description": "在文档库中搜索相关片段，返回匹配的文档内容和来源",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词或问题，用于在文档中检索相关内容",
                    }
                },
                "required": ["query"],
            },
        },
    },
]


def list_tables() -> str:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row["name"] for row in cursor.fetchall()]
    conn.close()
    return json.dumps(tables, ensure_ascii=False)


def describe_table(table_name: str) -> str:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,),
    )
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return f"表 '{table_name}' 不存在"
    return row["sql"]


def run_query(sql: str) -> str:
    sql_stripped = sql.strip()
    upper_sql = sql_stripped.upper()

    allowed_keywords = ("SELECT", "WITH", "EXPLAIN", "PRAGMA")
    if not any(upper_sql.startswith(kw) for kw in allowed_keywords):
        return f"错误：只允许只读查询（SELECT/WITH/EXPLAIN/PRAGMA），被拒绝的 SQL: {sql_stripped[:100]}"

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_stripped)
        rows = cursor.fetchall()
        if not rows:
            result = "(查询成功，但没有返回数据)"
        else:
            columns = [desc[0] for desc in cursor.description]
            lines = [",".join(columns)]
            for row in rows:
                lines.append(",".join(str(v) if v is not None else "NULL" for v in row))
            result = "\n".join(lines)
        conn.close()
        return result
    except Exception as e:
        conn.close()
        return f"SQL 执行错误: {str(e)}"


def search_docs(query: str) -> str:
    hits = search_docs_fn(query)
    if not hits:
        return "未找到相关文档内容。"
    lines = []
    for h in hits:
        lines.append(f"[来源: {h['source']}，相关度: {h['score']}]")
        lines.append(h["content"])
        lines.append("---")
    return "\n".join(lines)


def execute_tool(name: str, arguments: dict) -> str:
    if name == "list_tables":
        return list_tables()
    elif name == "describe_table":
        return describe_table(arguments["table_name"])
    elif name == "run_query":
        return run_query(arguments["sql"])
    elif name == "search_docs":
        return search_docs(arguments["query"])
    else:
        return f"未知工具: {name}"
