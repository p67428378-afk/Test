# Online Personal Loan Application

This project implements an online personal loan application system, consisting of a frontend web application and a backend API.

## Project Structure

- `frontend/`: Contains the React-based web application for loan applications.
- `backend/`: Contains the Python Flask API for processing loan applications, managing user data, and integrating with external services.

## Setup and Installation

Follow the instructions in the `frontend/README.md` and `backend/README.md` for detailed setup and running instructions for each part of the application.

## Features

- Secure capture and validation of personal information.
- Collection and verification of employment details.
- Specification of loan request details with constraints.
- Gathering of legal and citizenship information.
- Application submission and immediate confirmation.
- Integration with third-party services for identity verification, credit scoring, and income verification (planned).
- Secure handling of sensitive data (encryption, audit trails).
- User-friendly, responsive web form for application.

## Technologies

**Frontend:**
- React
- HTML/CSS
- JavaScript

**Backend:**
- Python
- Flask
- SQLAlchemy (ORM)
- PostgreSQL (Database)

## Deployment

The application is designed for deployment on Google Cloud Platform (GCP) using microservices architecture, Docker, and Kubernetes (GKE).

## Security

- HTTPS/SSL for all data in transit.
- Encryption at rest for sensitive data (SSN, income).
- Role-based access control (RBAC).
- Multi-Factor Authentication (MFA) for internal users.
- Regular security audits and penetration testing.
- Compliance with relevant financial regulations (GDPR, CCPA, GLBA).
