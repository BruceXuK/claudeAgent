import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "ecommerce.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            city TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            total_price REAL NOT NULL,
            order_date TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    # Only seed if tables are empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        _seed_data(conn)

    conn.commit()
    conn.close()


def _seed_data(conn: sqlite3.Connection):
    cursor = conn.cursor()

    users = [
        ("张三", "zhangsan@example.com", "北京"),
        ("李四", "lisi@example.com", "上海"),
        ("王五", "wangwu@example.com", "广州"),
        ("赵六", "zhaoliu@example.com", "深圳"),
        ("孙七", "sunqi@example.com", "杭州"),
        ("周八", "zhouba@example.com", "成都"),
        ("吴九", "wujiu@example.com", "武汉"),
        ("郑十", "zhengshi@example.com", "南京"),
        ("冯十一", "fengshiyi@example.com", "重庆"),
        ("陈十二", "chenshier@example.com", "北京"),
        ("褚十三", "chushisan@example.com", "上海"),
        ("卫十四", "weishisi@example.com", "广州"),
        ("蒋十五", "jiangshiwu@example.com", "深圳"),
        ("沈十六", "shenshiliu@example.com", "杭州"),
        ("韩十七", "hanshiqi@example.com", "成都"),
        ("杨十八", "yangshiba@example.com", "武汉"),
        ("朱十九", "zhushijiu@example.com", "南京"),
        ("秦二十", "qinershi@example.com", "重庆"),
        ("许二一", "xueryi@example.com", "北京"),
        ("何二二", "heerer@example.com", "上海"),
    ]
    cursor.executemany(
        "INSERT INTO users (name, email, city) VALUES (?, ?, ?)", users
    )

    products = [
        ("机械键盘", "电子产品", 399.00, 120),
        ("无线鼠标", "电子产品", 89.00, 300),
        ("显示器支架", "办公用品", 159.00, 80),
        ("Type-C 数据线", "电子产品", 29.90, 500),
        ("人体工学椅", "办公用品", 1299.00, 30),
        ("降噪耳机", "电子产品", 599.00, 60),
        ("笔记本支架", "办公用品", 79.00, 150),
        ("USB 扩展坞", "电子产品", 199.00, 90),
        ("护眼台灯", "办公用品", 259.00, 45),
        ("移动硬盘 1TB", "电子产品", 459.00, 70),
        ("双肩背包", "生活用品", 199.00, 100),
        ("保温杯", "生活用品", 69.00, 200),
        ("电动牙刷", "生活用品", 149.00, 85),
        ("瑜伽垫", "运动户外", 89.00, 120),
        ("运动手环", "电子产品", 249.00, 110),
        ("充电宝", "电子产品", 129.00, 180),
        ("桌面风扇", "生活用品", 49.00, 250),
        ("机械手表", "生活用品", 899.00, 20),
        ("跑步鞋", "运动户外", 499.00, 65),
        ("蓝牙音箱", "电子产品", 179.00, 95),
    ]
    cursor.executemany(
        "INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
        products,
    )

    orders = [
        (1, 1, 2, 798.00, "2025-01-15 10:30:00"),
        (1, 3, 1, 159.00, "2025-01-20 14:20:00"),
        (2, 2, 1, 89.00, "2025-02-03 09:15:00"),
        (2, 6, 1, 599.00, "2025-02-14 16:45:00"),
        (3, 1, 1, 399.00, "2025-02-20 11:00:00"),
        (3, 5, 1, 1299.00, "2025-03-01 08:30:00"),
        (4, 4, 3, 89.70, "2025-03-10 13:00:00"),
        (4, 8, 1, 199.00, "2025-03-15 17:20:00"),
        (5, 10, 1, 459.00, "2025-03-22 10:10:00"),
        (5, 12, 2, 138.00, "2025-04-01 15:30:00"),
        (6, 15, 1, 249.00, "2025-04-05 12:00:00"),
        (6, 18, 1, 899.00, "2025-04-10 09:45:00"),
        (7, 20, 1, 179.00, "2025-04-18 14:30:00"),
        (7, 17, 1, 49.00, "2025-04-22 11:15:00"),
        (8, 14, 1, 89.00, "2025-05-01 16:00:00"),
        (8, 19, 1, 499.00, "2025-05-08 10:30:00"),
        (9, 9, 1, 259.00, "2025-05-12 13:45:00"),
        (9, 11, 1, 199.00, "2025-05-18 09:00:00"),
        (10, 13, 1, 149.00, "2025-05-20 15:20:00"),
        (10, 16, 2, 258.00, "2025-05-25 11:00:00"),
        (11, 2, 2, 178.00, "2025-01-08 10:00:00"),
        (11, 7, 1, 79.00, "2025-02-12 14:00:00"),
        (12, 5, 1, 1299.00, "2025-03-05 09:30:00"),
        (12, 20, 1, 179.00, "2025-03-28 16:00:00"),
        (13, 1, 1, 399.00, "2025-04-15 11:30:00"),
        (13, 3, 2, 318.00, "2025-04-25 10:00:00"),
        (14, 6, 1, 599.00, "2025-05-02 13:00:00"),
        (14, 10, 1, 459.00, "2025-05-15 08:30:00"),
        (15, 12, 3, 207.00, "2025-05-22 17:00:00"),
        (15, 15, 1, 249.00, "2025-05-28 12:00:00"),
        (16, 8, 1, 199.00, "2025-01-22 09:00:00"),
        (16, 9, 1, 259.00, "2025-02-15 10:30:00"),
        (17, 18, 1, 899.00, "2025-03-18 14:00:00"),
        (17, 19, 1, 499.00, "2025-04-08 16:30:00"),
        (18, 14, 2, 178.00, "2025-04-30 11:00:00"),
        (18, 16, 1, 129.00, "2025-05-10 09:30:00"),
        (19, 4, 5, 149.50, "2025-05-20 15:00:00"),
        (19, 7, 1, 79.00, "2025-05-27 10:00:00"),
        (20, 11, 1, 199.00, "2025-01-05 13:00:00"),
        (20, 13, 2, 298.00, "2025-02-18 09:00:00"),
    ]
    cursor.executemany(
        "INSERT INTO orders (user_id, product_id, quantity, total_price, order_date) VALUES (?, ?, ?, ?, ?)",
        orders,
    )
