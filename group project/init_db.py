import sqlite3
import os

# Define database path (same as in app.py)
BASE_DIR = os.path.dirname(__file__)
db_dir = os.path.join(BASE_DIR, 'database')
os.makedirs(db_dir, exist_ok=True)
db_path = os.path.join(db_dir, 'tasks.db')

# Connect to the SQLite database (creates it if not existing)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop existing table (optional)
cursor.execute('DROP TABLE IF EXISTS tasks')

# Create the main tasks table
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    due_date TEXT,
    status TEXT DEFAULT 'pending'
)
''')

# Insert sample tasks
sample_tasks = [
    ('Math Assignment', 'Complete calculus homework', 'Mathematics', '2025-10-15', 'pending'),
    ('Science Project', 'Prepare chemistry presentation', 'Science', '2025-10-20', 'pending'),
    ('Essay Writing', 'Write an essay on climate change', 'English', '2025-10-25', 'completed')
]
cursor.executemany('INSERT INTO tasks (title, description, category, due_date, status) VALUES (?, ?, ?, ?, ?)', sample_tasks)

# Commit and close connection
conn.commit()
conn.close()

print("✅ Database 'tasks.db' created successfully in the 'database' folder with sample data.")