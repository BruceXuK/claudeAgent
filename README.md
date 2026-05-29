# SQL 问答智能体

基于 DeepSeek API 的 ReAct Agent，用自然语言查询 SQLite 数据库。

## 快速开始

```bash
export DEEPSEEK_API_KEY="sk-xxx"
pip install -r requirements.txt
python main.py
```

## 工作原理

```
用户提问 → ReAct 循环 → 回答

ReAct 循环（最多 8 轮）：
  1. 发送消息给 DeepSeek
  2. 模型决定：调用工具 OR 给出回答
  3. 如果调用工具 → 执行 → 结果反馈 → 回到步骤 1
  4. 如果给出回答 → 输出给用户
```

## 工具

| 工具 | 功能 |
|------|------|
| `list_tables` | 列出所有表名 |
| `describe_table` | 查看表结构 |
| `run_query` | 执行 SELECT 查询（只读） |

## 示例数据

首次运行自动创建 `ecommerce.db`，包含三张表：

- **users** — 用户（20 条）
- **products** — 商品（20 条）
- **orders** — 订单（40 条）

## 示例问题

```
> 数据库里有哪些表？
> 每个城市有多少用户？
> 哪个商品卖得最好？
> 上个月销售额最高的是哪一天？
> 客单价最高的用户是谁？
```
