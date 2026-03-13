# User Login and Welcome Page Redirection (SCRUM-46)

This project implements a secure user login system and redirects authenticated users to a welcome page, as specified in Jira issue SCRUM-46 and its associated High-Level Design (HLD).

## Features

*   User login with email and password.
*   Secure password hashing using `werkzeug.security`.
*   Session management with HttpOnly, Secure, and SameSite cookies.
*   Redirection to a welcome page upon successful login.
*   Generic error messages for invalid login attempts to prevent enumeration attacks.
*   Basic rate limiting for login attempts.

## Technologies Used

*   **Flask**: Web framework for the backend.
*   **Werkzeug**: For secure password hashing and session management.
*   **Python-dotenv**: For managing environment variables.

## Setup Instructions

### Prerequisites

*   Python 3.8+
*   Docker (optional, for containerized deployment)

### Local Development

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/p67428378-afk/Test.git
    cd Test
    git checkout ISSUE-SCRUM-46
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    Create a `.env` file in the root directory based on `.env.example`:
    ```ini
    # .env
    SECRET_KEY='your_very_secret_key_here'
    ```
    **Important:** Replace `'your_very_secret_key_here'` with a strong, randomly generated secret key.

5.  **Run the application:**
    ```bash
    flask run
    ```
    The application will be accessible at `http://127.0.0.1:5000`.

### Docker Deployment

1.  **Build the Docker image:**
    ```bash
    docker build -t user-login-app:latest .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -p 5000:5000 -e SECRET_KEY='your_very_secret_key_here' user-login-app:latest
    ```
    The application will be accessible at `http://localhost:5000`.

## Usage

1.  Navigate to `http://127.0.0.1:5000/login` (or `http://localhost:5000/login` if using Docker).
2.  Use the following credentials for testing:
    *   **Email:** `test@example.com`
    *   **Password:** `password123`
3.  Upon successful login, you will be redirected to the `/welcome` page.
4.  Attempting to log in with invalid credentials will display a generic error message.

## Architecture Notes

This implementation follows the HLD for SCRUM-46, providing a basic Flask application with in-memory user and session management for demonstration purposes. In a production environment, this would be replaced with a persistent database (e.g., PostgreSQL) for user data and a dedicated session store (e.g., Redis) for session management, as outlined in the HLD.

Security considerations like HTTPS, robust rate limiting, and comprehensive error handling are partially implemented and should be further enhanced for production deployment.
