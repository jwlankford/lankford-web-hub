import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "lankford_hub.db")
print(f"[SYSTEM] Connecting to database at {db_path}...")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE research_papers ADD COLUMN used_for VARCHAR;")
    print("Successfully added used_for column.")
except sqlite3.OperationalError as e:
    print(f"Error (maybe column already exists?): {e}")

conn.commit()
conn.close()
