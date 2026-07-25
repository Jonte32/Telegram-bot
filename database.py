"""
database.py
Handles all SQLite storage for the shop bot: products, orders, and cart persistence.
Using SQLite keeps this dependency-free and works fine for a small/medium shop bot.
"""
import sqlite3
import json
from datetime import datetime

DB_PATH = "shop.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist. Call this once on startup."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image_url TEXT,
            category_id INTEGER,
            in_stock INTEGER DEFAULT 1,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            language TEXT DEFAULT 'en'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            full_name TEXT,
            phone TEXT,
            address TEXT,
            items_json TEXT NOT NULL,
            total REAL NOT NULL,
            status TEXT DEFAULT 'new',
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------- Users / language preference ----------

def get_user_language(user_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT language FROM users WHERE user_id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return row["language"] if row else None


def set_user_language(user_id, language):
    conn = get_connection()
    conn.execute(
        """INSERT INTO users (user_id, language) VALUES (?, ?)
           ON CONFLICT(user_id) DO UPDATE SET language = excluded.language""",
        (user_id, language),
    )
    conn.commit()
    conn.close()


# ---------- Categories ----------

def add_category(name):
    conn = get_connection()
    try:
        conn.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,))
        conn.commit()
    finally:
        conn.close()


def get_categories():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM categories ORDER BY name").fetchall()
    conn.close()
    return rows


def get_or_create_category(name):
    conn = get_connection()
    row = conn.execute("SELECT id FROM categories WHERE name = ?", (name,)).fetchone()
    if row:
        conn.close()
        return row["id"]
    cur = conn.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    conn.commit()
    cat_id = cur.lastrowid
    conn.close()
    return cat_id


# ---------- Products ----------

def add_product(name, description, price, image_url, category_name):
    category_id = get_or_create_category(category_name)
    conn = get_connection()
    conn.execute(
        "INSERT INTO products (name, description, price, image_url, category_id) VALUES (?, ?, ?, ?, ?)",
        (name, description, price, image_url, category_id),
    )
    conn.commit()
    conn.close()


def get_products_by_category(category_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM products WHERE category_id = ? AND in_stock = 1 ORDER BY name",
        (category_id,),
    ).fetchall()
    conn.close()
    return rows


def get_product(product_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()
    return row


def remove_product(product_id):
    conn = get_connection()
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()


def get_all_products():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    conn.close()
    return rows


# ---------- Orders ----------

def create_order(user_id, username, full_name, phone, address, items, total):
    conn = get_connection()
    conn.execute(
        """INSERT INTO orders
           (user_id, username, full_name, phone, address, items_json, total, status, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, 'new', ?)""",
        (
            user_id,
            username,
            full_name,
            phone,
            address,
            json.dumps(items),
            total,
            datetime.utcnow().isoformat(),
        ),
    )
    conn.commit()
    order_id = conn.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
    conn.close()
    return order_id


def get_recent_orders(limit=10):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM orders ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return rows


def update_order_status(order_id, status):
    conn = get_connection()
    conn.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
    conn.commit()
    conn.close()
