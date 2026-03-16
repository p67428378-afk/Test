# Backend Service for Online Personal Loan Application

This directory contains the backend Flask application for the Online Personal Loan Application system.

## Technologies Used

- Python 3.9+
- Flask (Web Framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- python-dotenv (for environment variables)

## Setup and Installation

1.  **Prerequisites:**
    *   Python 3.9 or higher.
    *   A PostgreSQL database instance. Make sure you have the database URL.

2.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd backend
    ```

3.  **Create a virtual environment and activate it:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Environment Variables:**
    Create a `.env` file in the `backend/` directory with the following content:
    ```
    DATABASE_URL="postgresql://user:password@host:port/database_name"
    SECRET_KEY="your_super_secret_key_for_flask_sessions"
    ```
    Replace the placeholder values with your actual PostgreSQL connection string and a strong secret key.

6.  **Run the application:**
    ```bash
    flask run
    ```
    The application will typically run on `http://127.0.0.1:5000`.

## Database Migrations

Currently, the application uses `Base.metadata.create_all(engine)` to create tables on startup. For production environments, it is recommended to use a proper migration tool like Alembic.

## API Endpoints

(To be documented as endpoints are added)

- `GET /`: Basic health check.
