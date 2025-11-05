import sqlite3

from config import db_name


def create_table(db=db_name):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, db=db_name):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (user_id) VALUES (?)
        ''', (user_id,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

def get_all_users(db=db_name):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users')
    users = cursor.fetchall()
    conn.close()
    user_ids = [user[0] for user in users]
    return user_ids
