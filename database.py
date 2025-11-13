import sqlite3
from config import db_name

def create_table(db=db_name):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            english_level TEXT DEFAULT 'A1'
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, english_level="A1", db=db_name):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (user_id, english_level) VALUES (?, ?)
        ''', (user_id, english_level))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

def get_all_users(db=db_name):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, english_level FROM users')
    users = cursor.fetchall()
    conn.close()
    return users  # returns list of tuples (user_id, english_level)

def set_level(user_id, english_level, db=db_name):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET english_level = ? WHERE user_id = ?
    ''', (english_level, user_id))
    conn.commit()
    conn.close()

def get_level(user_id, db=db_name):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('SELECT english_level FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None