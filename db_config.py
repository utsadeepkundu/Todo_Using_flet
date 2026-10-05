import sqlite3

def create_connection() -> sqlite3.Connection:      # connecting (creating or opening) to a database
    return sqlite3.connect("TasksDB.db")

def create_table():
    con: sqlite3.Connection = create_connection()   # connecting to database
    cursor: sqlite3.Cursor = con.cursor()           # cursor is responsible to make changes in database
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS tasks (
            task_no INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            start TEXT NOT NULL,
            deadline TEXT NOT NULL,
            status INTEGER NOT NULL DEFAULT 0,
            notify INTEGER NOT NULL DEFAULT 0,
            priority INTEGER NOT NULL DEFAULT 0,
            description TEXT,
            notified_sent INTEGER NOT NULL DEFAULT 0
        )
    ''')
    con.commit()                                    # saving all changes
    con.close()                                     # disconnect from database