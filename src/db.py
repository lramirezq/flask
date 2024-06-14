import sqlite3

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("events.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn

def create_table():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS event (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT NOT NULL,
        event_name TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    print("Database initialized and table created.")
