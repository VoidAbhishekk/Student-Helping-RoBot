import sqlite3
from datetime import datetime

DB_PATH = "users.db"


def _connect():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


def _init_db():
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                username TEXT,
                registered_at TEXT
            )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS premium_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            access_key TEXT UNIQUE NOT NULL,
            used INTEGER DEFAULT 0,
            used_by INTEGER,
            created_on TEXT
        )
        """)
        columns = {row["name"] for row in conn.execute("PRAGMA table_info(users)")}
        if "registered_at" not in columns:
            conn.execute("ALTER TABLE users ADD COLUMN registered_at TEXT")
        columns = {row["name"] for row in conn.execute("PRAGMA table_info(users)")}

        if "is_premium" not in columns:
            conn.execute(
                "ALTER TABLE users ADD COLUMN is_premium INTEGER DEFAULT 0"
            )
            conn.execute(
                "UPDATE users SET registered_at = ? WHERE registered_at IS NULL",
                (datetime.now().strftime("%Y-%m-%d"),),
            )
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bot_settings (
                setting_key TEXT PRIMARY KEY,
                setting_value TEXT
            )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS premium_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            access_key TEXT UNIQUE NOT NULL,
            used INTEGER DEFAULT 0,
            used_by INTEGER,
            created_on TEXT
        )
        """)


_init_db()


def add_user(user):
    today = datetime.now().strftime("%Y-%m-%d")
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO users (user_id, first_name, username, registered_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                first_name = excluded.first_name,
                username = excluded.username
            """,
            (user.id, user.first_name, user.username, today),
        )


def get_user(user_id):
    with _connect() as conn:
        row = conn.execute(
            "SELECT user_id, first_name, username, registered_at FROM users WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        return dict(row) if row else None


def total_users():
    with _connect() as conn:
        return conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]


def get_all_users():
    with _connect() as conn:
        rows = conn.execute("SELECT user_id FROM users").fetchall()
        return [(row["user_id"],) for row in rows]


def save_latest_update(message):
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO bot_settings (setting_key, setting_value)
            VALUES ('latest_update', ?)
            ON CONFLICT(setting_key) DO UPDATE SET setting_value = excluded.setting_value
            """,
            (message,),
        )


def get_latest_update():
    with _connect() as conn:
        row = conn.execute(
            "SELECT setting_value FROM bot_settings WHERE setting_key = 'latest_update'"
        ).fetchone()
        return row["setting_value"] if row else None


def save_premium_key(access_key):
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO premium_keys
            (access_key, created_on)
            VALUES (?, ?)
            """,
            (
                access_key,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )

def get_premium_key(access_key):
    with _connect() as conn:
        return conn.execute(
            """
            SELECT *
            FROM premium_keys
            WHERE access_key = ?
            """,
            (access_key,),
        ).fetchone()

def mark_key_used(access_key, user_id):
    with _connect() as conn:
        conn.execute(
            """
            UPDATE premium_keys
            SET used = 1,
                used_by = ?
            WHERE access_key = ?
            """,
            (user_id, access_key),
        )

def make_user_premium(user_id):
    with _connect() as conn:
        conn.execute(
            """
            UPDATE users
            SET is_premium = 1
            WHERE user_id = ?
            """,
            (user_id,),
        )

def is_user_premium(user_id):
    with _connect() as conn:
        row = conn.execute(
            """
            SELECT is_premium
            FROM users
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

    return bool(row and row["is_premium"])
