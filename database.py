import sqlite3

conn = sqlite3.connect("users.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

    user_id INTEGER PRIMARY KEY,
    first_name TEXT,
    username TEXT

)
""")

conn.commit()


def add_user(user):

    cursor.execute(

        """
        INSERT OR IGNORE INTO users
        VALUES(?,?,?)
        """,

        (

            user.id,
            user.first_name,
            user.username

        )

    )

    conn.commit()


def total_users():

    cursor.execute(

        "SELECT COUNT(*) FROM users"

    )

    return cursor.fetchone()[0]


def get_all_users():

    cursor.execute(

        "SELECT user_id FROM users"

    )

    return cursor.fetchall()