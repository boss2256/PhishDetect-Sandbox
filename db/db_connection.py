import sqlite3
from contextlib import closing

def connect_db():
    conn = sqlite3.connect("user_inputs.db")
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS UserInputs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            website TEXT,
                            field_name TEXT,
                            field_value TEXT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                        )''')
    return conn

def query_dynamic_user_inputs(website=None, field_name=None):
    query = "SELECT * FROM UserInputs WHERE 1=1"
    params = []
    if website:
        query += " AND website = ?"
        params.append(website)
    if field_name:
        query += " AND field_name = ?"
        params.append(field_name)

    with connect_db() as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()
    return results
