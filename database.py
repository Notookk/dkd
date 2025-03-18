import sqlite3

# Database Connection
conn = sqlite3.connect("bot_data.db", check_same_thread=False)
cursor = conn.cursor()

# Create Tables
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    first_name TEXT
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS sudo_users (
    user_id INTEGER PRIMARY KEY
)""")

conn.commit()

# Add User to Database
def add_user(user_id, first_name):
    cursor.execute("INSERT OR IGNORE INTO users (user_id, first_name) VALUES (?, ?)", (user_id, first_name))
    conn.commit()

# Get User Info
def get_user_info(user_id):
    cursor.execute("SELECT first_name FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()
    if user:
        return f"👤 User: {user[0]}\n🆔 ID: {user_id}"
    return "⚠️ User not found in the database."

# Add Sudo User
def add_sudo(user_id):
    cursor.execute("INSERT OR IGNORE INTO sudo_users (user_id) VALUES (?)", (user_id,))
    conn.commit()

# Remove Sudo User
def remove_sudo(user_id):
    cursor.execute("DELETE FROM sudo_users WHERE user_id=?", (user_id,))
    conn.commit()

# List Sudo Users
def list_sudo_users():
    cursor.execute("SELECT user_id FROM sudo_users")
    users = cursor.fetchall()
    if users:
        return "\n".join([f"👑 {user[0]}" for user in users])
    return "⚠️ No sudo users found."
