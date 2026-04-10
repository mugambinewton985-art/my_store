import sqlite3

conn = sqlite3.connect("store.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    description TEXT NOT NULL
)
""")

# Sample products
c.execute("INSERT INTO products (name, price, description) VALUES (?, ?, ?)",
          ("Laptop", 50000, "High performance laptop"))

c.execute("INSERT INTO products (name, price, description) VALUES (?, ?, ?)",
          ("Phone", 20000, "Latest smartphone"))

c.execute("INSERT INTO products (name, price, description) VALUES (?, ?, ?)",
          ("Headphones", 5000, "Noise cancelling headphones"))

conn.commit()
conn.close()

print("Database created!")
