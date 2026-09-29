import sqlite3

conn = sqlite3.connect("realestate.db")
cursor = conn.cursor()

# Properties Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS properties (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    type TEXT,
    city TEXT,
    area TEXT,
    bhk TEXT,
    price INTEGER,
    status TEXT,
    image TEXT

)
""")

# Leads Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS leads (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,
    phone TEXT,
    message TEXT

)
""")

# Bookings Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,
    phone TEXT,
    property TEXT,
    date TEXT,
    time TEXT

)
""")

# Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,
    password TEXT

)
""")

cursor.execute("""
INSERT OR IGNORE INTO users
(id, username, password)

VALUES
(1,'admin','admin123')
""")

conn.commit()
conn.close()

print("Database Created Successfully")