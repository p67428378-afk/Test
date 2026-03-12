# Guest Room Booking System

## Project Overview
This project implements a Guest Room Booking System, enabling hotel guests to search for available rooms, select preferred room types, and securely make payments. The system is designed with a microservices architecture, a relational database for data management, and a responsive frontend user interface.

## Architecture
The system is composed of several microservices, an API Gateway, a relational database, and a frontend application:

1.  **API Gateway**: Acts as the single entry point for all client requests, handling request routing, SSL termination, authentication, and rate limiting.
2.  **Search Service**: Dedicated microservice for handling high-volume read queries related to room availability, filtering, and pricing.
3.  **Booking Service**: Manages reservation logic, booking state transitions (pending, paid, canceled), and updates room inventory.
4.  **Payment Service**: Handles secure transaction processing, supporting various payment methods and integrating with a PCI-compliant payment gateway.
5.  **Database**: A robust relational database stores all system data, including hotel information, room types, user profiles, booking details, and payment records.
6.  **Frontend Application**: A responsive web interface that consumes the backend APIs to provide a seamless user experience for searching, selecting, and booking rooms.

## Setup Instructions

### Prerequisites
- Docker and Docker Compose (for local development)
- Python 3.9+
- Node.js (for frontend development)
- PostgreSQL (or other relational database)

### Backend Setup (Python Microservices)
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/p67428378-afk/Test.git
    cd Test
    ```
2.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
3.  **Set up virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
4.  **Configure environment variables:**
    Create a `.env` file in the `backend` directory based on `.env.example`.
    ```
    # Example .env content
    DATABASE_URL="postgresql://user:password@db:5432/booking_db"
    PAYMENT_GATEWAY_API_KEY="your_payment_gateway_api_key"
    # ... other service-specific variables
    ```
5.  **Run database migrations:**
    (Specific commands will depend on the ORM chosen, e.g., Alembic for SQLAlchemy)
    ```bash
    # Example: alembic upgrade head
    ```
6.  **Start the backend services:**
    ```bash
    python main.py # Or use Docker Compose for all services
    ```

### Frontend Setup (React/Vue/Angular - TBD)
1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install # or yarn install
    ```
3.  **Configure environment variables:**
    Create a `.env` file based on `.env.example`.
    ```
    # Example .env content
    REACT_APP_API_GATEWAY_URL="http://localhost:8000"
    ```
4.  **Start the frontend application:**
    ```bash
    npm start # or yarn start
    ```

### Docker Compose (for integrated local development)
A `docker-compose.yml` file will be provided to orchestrate all services (backend, database, frontend, API Gateway) for easy local setup.
```bash
docker-compose up --build
```

## Usage Examples
(To be filled in with API endpoints and frontend interaction flows once implemented)

## API Endpoints (Planned)

### Search Service
-   `GET /api/v1/rooms/search?check_in_date=...&check_out_date=...&guests=...`: Search for available rooms.

### Booking Service
-   `POST /api/v1/bookings`: Create a new booking.
-   `GET /api/v1/bookings/{booking_id}`: Retrieve booking details.
-   `PUT /api/v1/bookings/{booking_id}/cancel`: Cancel a booking.

### Payment Service
-   `POST /api/v1/payments`: Process a payment for a booking.
-   `GET /api/v1/payments/{payment_id}`: Retrieve payment status.

## Database Schema (Planned Key Tables)
-   `hotels`: Stores hotel information.
-   `room_types`: Defines different room categories (e.g., Standard King, Deluxe Queen).
-   `rooms`: Individual physical rooms, linked to `room_types`.
-   `users`: User profiles.
-   `bookings`: Records of guest reservations.
-   `payments`: Transaction details.
-   `room_type_inventory`: Tracks availability and pricing for room types on specific dates.

## Contributing
(To be added)

## License
(To be added)
