import sqlite3

# Connect to the existing database
conn = sqlite3.connect("security_permanent.db")
cursor = conn.cursor()

# Fetch all employee records
cursor.execute("SELECT id, employee_id, name, face_image FROM employees")
rows = cursor.fetchall()

print("✅ Database test successful!")
print(f"Found {len(rows)} employees:\n")

for row in rows:
    print(f"ID: {row[0]} | Employee ID: {row[1]} | Name: {row[2]} | Image: {row[3]}")

conn.close()