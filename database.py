import sqlite3
from config import db_name

def create_tables(db=db_name):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            english_level TEXT DEFAULT 'A1'
        );

        CREATE TABLE IF NOT EXISTS texts (
            text_id INTEGER PRIMARY KEY AUTOINCREMENT,
            english_level TEXT NOT NULL,
            content TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS words (
            word_id INTEGER PRIMARY KEY AUTOINCREMENT,
            english_level TEXT NOT NULL,
            word TEXT NOT NULL,
            translation TEXT NOT NULL,
            example TEXT
        );

        CREATE TABLE IF NOT EXISTS level_stats (
            english_level TEXT PRIMARY KEY,
            num_texts INTEGER DEFAULT 0,
            num_words INTEGER DEFAULT 0
        );
        """)
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
    return users

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

def get_users_full(db=db_name):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""
        SELECT english_level, user_id
        FROM users
        ORDER BY english_level, user_id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def add_text(english_level, content, db=db_name):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("INSERT INTO texts (english_level, content) VALUES (?, ?)",
                (english_level, content))
    cur.execute("""
        INSERT INTO level_stats (english_level, num_texts, num_words)
        VALUES (?, 1, 0)
        ON CONFLICT(english_level) DO UPDATE SET num_texts = num_texts + 1
    """, (english_level,))
    conn.commit()
    conn.close()

def add_word(english_level, word, translation, example, db=db_name):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("INSERT INTO words (english_level, word, translation, example) VALUES (?, ?, ?, ?)",
                (english_level, word, translation, example))
    cur.execute("""
        INSERT INTO level_stats (english_level, num_texts, num_words)
        VALUES (?, 0, 1)
        ON CONFLICT(english_level) DO UPDATE SET num_words = num_words + 1
    """, (english_level,))
    conn.commit()
    conn.close()

def get_text(english_level, n, db=db_name):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""
        SELECT content
        FROM texts
        WHERE english_level = ?
        ORDER BY text_id
        LIMIT 1 OFFSET ?
    """, (english_level, n))
    text = cur.fetchone()
    conn.close()
    return text

def get_word(english_level, n, db=db_name):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""
        SELECT word, translation, example
        FROM words
        WHERE english_level = ?
        ORDER BY word_id
        LIMIT 1 OFFSET ?
    """, (english_level, n))
    word = cur.fetchone()
    conn.close()
    return word

def get_level_stats(english_level, db=db_name):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""
        SELECT num_texts, num_words
        FROM level_stats
        WHERE english_level = ?
    """, (english_level,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"num_texts": row[0], "num_words": row[1]}
    else:
        return {"num_texts": 0, "num_words": 0}