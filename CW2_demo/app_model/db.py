import sqlite3

def get_connection():
    return sqlite3.connect(
        "DATA/project_data.db",
        check_same_thread=False
    )