# setup_db.py
import os
from sqlalchemy import create_engine, text

# Your Render PostgreSQL URL (from Environment Variables or hardcode for now)
DATABASE_URL = "postgresql://rover_db_user:zc8qubBCgXNPUX51ulZVWsxvHOo0plL7@dpg-d44tah4hg0os73fn8reg-a.oregon-postgres.render.com/rover_db"

engine = create_engine(DATABASE_URL)

# Create employees table
create_table_sql = """
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    employee_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    position TEXT,
    department TEXT,
    phone TEXT,
    email TEXT,
    face_image TEXT
);
"""

# Insert sample data (only if table is empty)
insert_data_sql = """
INSERT INTO employees (employee_id, name, position, department, phone, email, face_image)
SELECT 'E001', 'Priyanshu Roy', 'Developer', 'Surveillance', '9883142407', 'priyanshuroy0912@gmail.com', 'faces/priyanshu.jpg'
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE employee_id = 'E001');

INSERT INTO employees (employee_id, name, position, department, phone, email, face_image)
SELECT 'E002', 'Rajasree Chakraborty', 'Developer', 'Surveillance', '6290855493', 'Chakrabortyrajasree23@gmail.com', 'faces/rajasree.jpg'
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE employee_id = 'E002');

INSERT INTO employees (employee_id, name, position, department, phone, email, face_image)
SELECT 'E003', 'Rishab Ganguly', 'Developer', 'Surveillance', '9433605543', 'rishabhsunny25@gmail.com', 'faces/rishab.jpg'
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE employee_id = 'E003');

INSERT INTO employees (employee_id, name, position, department, phone, email, face_image)
SELECT 'E004', 'Rishita Chakraborty', 'Developer', 'Surveillance', '8293270106', 'rishitac88@gmail.com', 'faces/rishita.jpg'
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE employee_id = 'E004');

INSERT INTO employees (employee_id, name, position, department, phone, email, face_image)
SELECT 'E005', 'Rudranil Chakraborty', 'Developer', 'Surveillance', '9434129622', 'rudranilchakraborty49@gmail.com', 'faces/rudranil.jpg'
WHERE NOT EXISTS (SELECT 1 FROM employees WHERE employee_id = 'E005');
"""

# Run it
with engine.connect() as conn:
    conn.execute(text(create_table_sql))
    conn.execute(text(insert_data_sql))
    conn.commit()
    print("✅ employees table created and sample data inserted!")