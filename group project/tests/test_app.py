import pytest
from app import app, init_db, get_db_connection

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()  # Initialize the database for testing
        yield client

def test_index(client):
    """Test the index route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Student Task Manager' in response.data

def test_add_task(client):
    """Test adding a new task."""
    response = client.post('/add', data={
        'title': 'Test Task',
        'description': 'Test Description',
        'category': 'Test Category',
        'due_date': '2025-12-31'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Task' in response.data

def test_complete_task(client):
    """Test marking a task as completed."""
    # First, add a task
    client.post('/add', data={
        'title': 'Task to Complete',
        'description': 'Description',
        'category': 'Category',
        'due_date': '2025-12-31'
    })
    # Get the task id (assuming it's the last one)
    conn = get_db_connection()
    task = conn.execute('SELECT id FROM tasks ORDER BY id DESC LIMIT 1').fetchone()
    conn.close()
    task_id = task['id']
    # Complete it
    response = client.get(f'/complete/{task_id}', follow_redirects=True)
    assert response.status_code == 200
    # Check status
    conn = get_db_connection()
    updated_task = conn.execute('SELECT status FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    assert updated_task['status'] == 'completed'