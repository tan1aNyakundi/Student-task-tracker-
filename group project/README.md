# Student Task Manager

A simple Flask web application for managing student tasks.

## Features

- Add, edit, and delete tasks
- Mark tasks as completed
- Categorize tasks
- Set due dates
- Responsive design

## Setup

1. Ensure you have Python installed.
2. Install Flask: `pip install flask`
3. Run the database initialization: `python init_db.py`
4. Run the app: `python app.py`
5. Open your browser to `http://127.0.0.1:5000/`

## Project Structure

- `app.py`: Main Flask application
- `init_db.py`: Database initialization script
- `templates/`: HTML templates
- `static/css/`: CSS stylesheets
- `database/`: SQLite database files
- `requirements.txt`: Python dependencies

## Deployment

To deploy this app to a hosting service for your lecturer to view the live website:

1. Create a GitHub repository and push your code (including `requirements.txt`).
2. Sign up for a free account on [Render](https://render.com/).
3. Create a new Web Service, connect your GitHub repo.
4. Set the following:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Deploy. Render will provide a live URL (e.g., https://your-app.onrender.com).

Alternatively, use Railway or Heroku. The app is configured for production deployment.