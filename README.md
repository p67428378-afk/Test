# Room Status Management System

This project implements a Room Status Management System as described in Jira issue SCRUM-42 and its High-Level Design (HLD). The system provides a backend API for managing room statuses (vacant, occupied, out-of-order) and integrates with a PostgreSQL database.

## Architecture Overview

The system is designed with a microservices architecture, featuring:
- **Room Status Service:** A Flask-based microservice handling room status logic and API endpoints.
- **PostgreSQL Database:** For persistent storage of room information, statuses, and logs.

## Getting Started

### Prerequisites

- Python 3.9+
- Docker (optional, for containerized deployment)
- PostgreSQL (or a Dockerized PostgreSQL instance)

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/p67428378-afk/Test.git
    cd Test
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Environment Variables:**
    Create a `.env` file based on `.env.example` and fill in the details.

    ```
    # .env
    DATABASE_URL="postgresql://user:password@host:port/database_name"
    SECRET_KEY="your_secret_key_for_flask"
    ```

4.  **Database Setup:**
    Ensure your PostgreSQL database is running and accessible. The application will automatically create tables if they don't exist when it starts.

### Running the Application

1.  **Activate your virtual environment:**
    ```bash
    source venv/bin/activate
    ```

2.  **Run the Flask application:**
    ```bash
    flask run
    ```

    The API will be available at `http://127.0.0.1:5000`.

## API Endpoints

### `GET /rooms`

Retrieves a list of all rooms with their current statuses.

### `GET /rooms/<room_id>`

Retrieves details of a specific room by its ID.

### `PUT /rooms/<room_id>/status`

Updates the status of a specific room.

**Request Body:**
```json
{
    "status": "vacant" | "occupied" | "out-of-order",
    "reason": "Guest checked out"
}
```

**Status Transition Rules:**
- Cannot transition directly from `out-of-order` to `occupied`. Must go through `vacant` first.

## Development

### Project Structure

```
.
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
└── app/
    ├── __init__.py
    ├── models.py
    ├── routes.py
    └── services.py
```

### Technologies Used

- **Backend:** Python, Flask, SQLAlchemy, Psycopg2
- **Database:** PostgreSQL
- **Containerization:** Docker

## Contributing

Please refer to the HLD and Jira issue SCRUM-42 for detailed requirements and design.
