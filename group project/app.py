from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__, static_folder='static')

# Database path
DATABASE = os.path.join(os.path.dirname(__file__), 'database', 'tasks.db')

def get_db_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database and create the tasks table if it doesn't exist."""
    db_dir = os.path.join(os.path.dirname(__file__), 'database')
    os.makedirs(db_dir, exist_ok=True)
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT,
                due_date TEXT,
                status TEXT DEFAULT 'pending'
            )
        ''')
        # Check if table is empty, if so, add sample data
        if not conn.execute('SELECT id FROM tasks LIMIT 1').fetchone():
            sample_tasks = [
                ('Math Assignment', 'Complete calculus homework', 'Mathematics', '2025-10-15', 'pending'),
                ('Science Project', 'Prepare chemistry presentation', 'Science', '2025-10-20', 'pending'),
                ('Essay Writing', 'Write an essay on climate change', 'English', '2025-10-25', 'completed')
            ]
            conn.executemany('INSERT INTO tasks (title, description, category, due_date, status) VALUES (?, ?, ?, ?, ?)', sample_tasks)
        conn.commit()

@app.route('/')
def index():
    """Display all tasks on the homepage."""
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY due_date').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    """Handle adding a new task."""
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        category = request.form.get('category', '')
        due_date = request.form.get('due_date', '')
        status = 'pending'

        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO tasks (title, description, category, due_date, status) VALUES (?, ?, ?, ?, ?)',
                         (title, description, category, due_date, status))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return render_template('add_task.html', error=str(e))
    return render_template('add_task.html')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """Handle editing an existing task."""
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        category = request.form.get('category', '')
        due_date = request.form.get('due_date', '')
        status = request.form.get('status', 'pending')

        conn.execute('UPDATE tasks SET title = ?, description = ?, category = ?, due_date = ?, status = ? WHERE id = ?',
                     (title, description, category, due_date, status, task_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_task.html', task=task)

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    """Mark a task as completed."""
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET status = ? WHERE id = ?', ('completed', task_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Delete a task."""
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Initialize database on startup
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)