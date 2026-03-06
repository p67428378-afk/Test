# Secure User Login (SCRUM-28)

## Project Overview
This project implements a secure user login system as a microservice, addressing the requirements outlined in Jira issue SCRUM-28 and its associated High-Level Design (HLD). The system focuses on robust authentication, secure session management, password reset functionality, and brute-force protection.

## Architecture
The system adopts a Microservices Architecture for the authentication component, leveraging AWS services for deployment. Key components include:
- **User Client:** (Out of scope for this implementation, but interacts with the API Gateway)
- **CDN / WAF:** (Conceptual, handled by AWS CloudFront/WAF in deployment)
- **API Gateway:** (Conceptual, handled by AWS API Gateway in deployment)
- **Authentication Service:** A Python-based microservice responsible for core login logic.
- **User Database:** PostgreSQL for storing user credentials.
- **Session Store:** Redis for managing user sessions.
- **Email Service:** For password reset functionality (placeholder/mock).
- **Monitoring & Logging:** For observability.

## In-Scope Features
- User authentication (username/password validation).
- Secure session management (creation, validation, termination).
- Password reset mechanism (via email verification).
- Brute-force protection (rate limiting, account lockout).
- Handling of invalid credentials with non-specific error messages.
- Secure storage of user credentials (password hashing).
- Secure communication protocols (HTTPS/SSL/TLS - conceptual for local dev).
- Server-side validation for login inputs.
- Logging of login attempts for auditing.

## Out-of-Scope Features
- User registration process.
- Advanced multi-factor authentication (MFA).
- Social logins (e.g., Google, Facebook).
- Single Sign-On (SSO) integration.
- Detailed UI/UX design beyond functional requirements.

## Setup Instructions

### Prerequisites
- Docker and Docker Compose
- Python 3.9+
- PostgreSQL
- Redis

### Local Development
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/p67428378-afk/Test.git
    cd Test
    ```
2.  **Create and configure environment variables:**
    Copy `.env.example` to `.env` and update the values.
    ```bash
    cp .env.example .env
    ```
3.  **Build and run with Docker Compose (recommended):**
    ```bash
    docker-compose up --build
    ```
    This will start the PostgreSQL database, Redis, and the Authentication Service.

4.  **Manual Setup (if not using Docker Compose):**
    a.  **Install Python dependencies:**
        ```bash
        pip install -r requirements.txt
        ```
    b.  **Start PostgreSQL and Redis servers.**
    c.  **Run database migrations:** (Details to be provided in a separate migration script)
    d.  **Run the application:**
        ```bash
        python src/main.py # Or equivalent command for your chosen framework
        ```

## Usage
(Details on how to interact with the API endpoints will be added here once implemented.)

## Architecture Notes
- The Authentication Service is designed as a stateless microservice.
- Passwords are hashed using bcrypt/Argon2 with unique salts.
- Sessions are managed using Redis and secure HTTP-only, SameSite cookies.
- Rate limiting and account lockout mechanisms are in place to prevent brute-force attacks.
