import sqlite3
from typing import List, Set

# Database file path
DATABASE_FILE = "bot_data.db"

# Initialize the database
def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Table for sudo users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sudo_users (
            user_id INTEGER PRIMARY KEY
        )
    """)
    
    # Table for exempt users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exempt_users (
            user_id INTEGER PRIMARY KEY
        )
    """)
    
    # Table for muted users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS muted_users (
            user_id INTEGER PRIMARY KEY,
            until_date DATETIME
        )
    """)
    
    conn.commit()
    conn.close()

# Add a sudo user
def add_sudo(user_id: int):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO sudo_users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

# Remove a sudo user
def remove_sudo(user_id: int):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sudo_users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

# List all sudo users
def list_sudo_users() -> List[int]:
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM sudo_users")
    sudo_users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return sudo_users

# Check if a user is a sudo user
def is_sudo_user(user_id: int) -> bool:
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM sudo_users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone() is not None
    conn.close()
    return result

# Add an exempt user
def add_exempt_user(user_id: int):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO exempt_users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

# Remove an exempt user
def remove_exempt_user(user_id: int):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM exempt_users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

# List all exempt users
def list_exempt_users() -> Set[int]:
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM exempt_users")
    exempt_users = {row[0] for row in cursor.fetchall()}
    conn.close()
    return exempt_users

# Add a muted user
def add_muted_user(user_id: int, until_date: str):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO muted_users (user_id, until_date) VALUES (?, ?)", (user_id, until_date))
    conn.commit()
    conn.close()

# Remove a muted user
def remove_muted_user(user_id: int):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM muted_users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

# Check if a user is muted
def is_muted_user(user_id: int) -> bool:
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM muted_users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone() is not None
    conn.close()
    return result

# Initialize the database when this module is imported
init_db()
