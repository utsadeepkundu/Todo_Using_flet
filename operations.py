import sqlite3
from db_config import create_connection


def add_task(task_name: str, start: str, deadline: str, description: str = "") -> bool:
    try:
        con: sqlite3.Connection = create_connection()
        cursor: sqlite3.Cursor = con.cursor()
        cursor.execute("INSERT INTO tasks(task_name, start, deadline, status, notify, priority, description) VALUES (?, ?, ?, ?, ?, ?, ?)", (task_name, start, deadline, 0, 0, 0, description))
        con.commit()
        con.close()
        print("task added successfully.")
        return True
    
    except sqlite3.Error:
        print(f"Error occurred while adding task.")
        return False


def get_tasks_list():
    con: sqlite3.Connection = create_connection()
    cursor: sqlite3.Cursor = con.cursor()
    cursor.execute("SELECT * from tasks")
    tasks: list = cursor.fetchall()
    con.close()
    return tasks


def search_task_name(task_name: str):
    con: sqlite3.Connection = create_connection()
    cursor: sqlite3.Cursor = con.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE task_name LIKE ? OR description LIKE ?",
        (f"{task_name}%", f"%{task_name}%")
    )

    tasks: list = cursor.fetchall()
    con.close()
    return tasks


def remove_a_task(task_no: int) -> bool:
    try:
        con: sqlite3.Connection = create_connection()
        cursor: sqlite3.Cursor = con.cursor()
        cursor.execute("DELETE FROM tasks WHERE task_no = ?", (task_no,))
        con.commit()
        con.close()
        print("Task removed successfully.")
        return True
    
    except sqlite3.Error:
        print("Error occurred while removing task.")
        return False


def delete_all_tasks():
    try:
        con: sqlite3.Connection = create_connection()
        cursor: sqlite3.Cursor = con.cursor()
        cursor.execute("DELETE FROM tasks")
        con.commit()
        con.close()
        print("All tasks deleted successfully.")
        return True
    
    except sqlite3.Error:
        print("Error occurred while deleting all tasks.")
        return False


def update_status(task_no: int, status: int) -> bool:       # 0, 1, 2
    try:
        con: sqlite3.Connection = create_connection()
        cursor: sqlite3.Cursor = con.cursor()
        cursor.execute("UPDATE tasks SET status = ? WHERE task_no = ?", (status, task_no))
        con.commit()
        con.close()
        print("Task status updated.")
        return True
    
    except sqlite3.Error:
        print("Error occurred while updating task status.")
        return False


def update_priority(task_no: int, priority: int) -> bool:       # 1 or 0
    try:
        con: sqlite3.Connection = create_connection()
        cursor: sqlite3.Cursor = con.cursor()
        cursor.execute("UPDATE tasks SET priority = ? WHERE task_no = ?", (priority, task_no))
        con.commit()
        con.close()
        print("Task priority updated.")
        return True
    
    except sqlite3.Error:
        print("Error occurred while updating task priority.")
        return False


def update_notify(task_no: int, notify: int) -> bool:       # 1 or 0
    try:
        con: sqlite3.Connection = create_connection()
        cursor: sqlite3.Cursor = con.cursor()
        cursor.execute("UPDATE tasks SET notify = ? WHERE task_no = ?", (notify, task_no))
        con.commit()
        con.close()
        print("Task notification updated.")
        return True
    
    except sqlite3.Error:
        print("Error occurred while updating task notification.")
        return False


def update_notified_sent(task_no: int, notified_sent: int) -> bool:       # 1 or 0
    try:
        con: sqlite3.Connection = create_connection()
        cursor: sqlite3.Cursor = con.cursor()
        cursor.execute("UPDATE tasks SET notified_sent = ? WHERE task_no = ?", (notified_sent, task_no))
        con.commit()
        con.close()
        print("Task notified_sent updated.")
        return True
    
    except sqlite3.Error:
        print("Error occurred while updating task notified_sent.")
        return False