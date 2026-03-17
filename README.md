# Loan Application Platform Backend

This project implements the backend services for a Loan Application Platform, focusing on loan application submission, status tracking, and document management, as defined in Jira issue SCRUM-57 and its associated High-Level Design (HLD).

## Architecture Overview

The system is designed with a microservices architecture, leveraging AWS services for deployment. Key components include:
- **Loan Application Service**: Manages the lifecycle of loan applications.
- **Document Management Service**: Handles secure upload, storage, and retrieval of supporting documents.

## Setup and Installation

### Prerequisites
- Python 3.8+
- pip (Python package installer)
- Docker (optional, for containerized deployment)

### Local Development

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/p67428378-afk/Test.git
    cd Test
    git checkout ISSUE-SCRUM-57
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    Create a `.env` file in the root directory based on `config.py` and populate it with necessary values (e.g., database connection string, S3 bucket details).

5.  **Run the application:**
    ```bash
    flask run
    ```
    The application will typically run on `http://127.0.0.1:5000`.

## API Endpoints

(To be detailed as endpoints are implemented)

## Project Structure

```
.
├── README.md
├── requirements.txt
├── config.py
├── .gitignore
├── Dockerfile
└── app/
    ├── __init__.py
    ├── main.py
    ├── models.py
    └── services/
        ├── __init__.py
        ├── loan_service.py
        └── document_service.py
```

## HLD Reference

The High-Level Design document can be found at: [https://bfsi-na-ai-engineering.atlassian.net/wiki/spaces/SCRUM1/pages/14712834](https://bfsi-na-ai-engineering.atlassian.net/wiki/spaces/SCRUM1/pages/14712834)
