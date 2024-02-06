# db.py
#
# Application: Routine Checking App
#
# Create by: Tu Nguyen Ngoc


import sqlite3
import os
import sys

DATABASE_PATH = 'routine_checking_app.db'

def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    return conn

# Function to get the correct path for a resource, works for both development and packaged app
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Then, in your `initialize_database` function, use the `resource_path` function
def initialize_database():
    """Initialize the database by creating tables based on the schema.sql file."""
    conn = get_db_connection()
    cursor = conn.cursor()

    schema_path = resource_path('database/schema.sql')  # Use the function to get the correct path
    with open(schema_path, 'r') as schema_file:
        schema_script = schema_file.read()

    cursor.executescript(schema_script)

    conn.commit()
    conn.close()

def get_or_create_daily_task_id(conn, date):
    """Get or create a DailyTask entry for a specific date and return its ID."""
    cur = conn.cursor()
    cur.execute("SELECT id FROM DailyTasks WHERE date = ?", (date,))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        cur.execute("INSERT INTO DailyTasks (date) VALUES (?)", (date,))
        conn.commit()
        return cur.lastrowid

def insert_task(conn, daily_task_id, name, type_of_task, is_done):
    """Insert a new task linked to a DailyTask entry, without specifying date here."""
    sql = ''' INSERT INTO Task(DailyTaskID, name, type_of_task, isDone)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (daily_task_id, name, type_of_task, is_done))
    conn.commit()
    return cur.lastrowid

def update_task(conn, task_id, name, type_of_task, is_done):
    """Update an existing task."""
    sql = ''' UPDATE Task
              SET name = ?, type_of_task = ?, isDone = ?
              WHERE id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (name, type_of_task, is_done, task_id))
    conn.commit()

def delete_task(conn, task_id):
    """Delete an existing task."""
    sql = 'DELETE FROM Task WHERE id = ?'
    cur = conn.cursor()
    cur.execute(sql, (task_id,))
    conn.commit()

def delete_daily_task_and_tasks(conn, date):
    """Delete a DailyTask and all associated tasks for a specific date."""
    cur = conn.cursor()
    cur.execute("SELECT id FROM DailyTasks WHERE date=?", (date,))
    daily_task_id = cur.fetchone()

    if daily_task_id:
        cur.execute("DELETE FROM Task WHERE DailyTaskID=?", (daily_task_id[0],))
        cur.execute("DELETE FROM DailyTasks WHERE id=?", (daily_task_id[0],))
        conn.commit()

def fetch_tasks_for_date(conn, date):
    """Fetch tasks for a specific date."""
    tasks = []
    cur = conn.cursor()
    # Get the DailyTaskID for the given date
    cur.execute("SELECT id FROM DailyTasks WHERE date=?", (date,))
    daily_task_result = cur.fetchone()
    if daily_task_result:
        daily_task_id = daily_task_result[0]
        # Fetch tasks associated with the DailyTaskID
        cur.execute("SELECT id, name, type_of_task, isDone FROM Task WHERE DailyTaskID=?", (daily_task_id,))
        tasks = cur.fetchall()
    return tasks
