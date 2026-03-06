from flask import Flask, request, jsonify, session
from dotenv import load_dotenv
import os
import redis
from datetime import datetime, timedelta
from passlib.hash import bcrypt
import psycopg2
import uuid

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "super-secret-key-for-session-management")

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "auth_db"),
        user=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASSWORD", "password")
    )
    return conn

# Redis connection for session management and rate limiting
redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0
)

# --- Helper Functions ---

def hash_password(password):
    return bcrypt.hash(password)

def verify_password(password, hashed_password):
    return bcrypt.verify(password, hashed_password)

def generate_session_id():
    return str(uuid.uuid4())

def set_session(user_id):
    session_id = generate_session_id()
    redis_client.setex(f"session:{session_id}", timedelta(hours=1), user_id)
    return session_id

def get_user_id_from_session(session_id):
    return redis_client.get(f"session:{session_id}")

def delete_session(session_id):
    redis_client.delete(f"session:{session_id}")

def send_password_reset_email(email, reset_token):
    # This is a placeholder. In a real application, integrate with an email service.
    print(f"Sending password reset email to {email} with token: {reset_token}")
    # Example using Flask-Mail or a direct SMTP client:
    # msg = Message("Password Reset Request", sender=os.getenv("EMAIL_FROM"), recipients=[email])
    # msg.body = f"Your password reset token is: {reset_token}. It expires in 15 minutes."
    # mail.send(msg)
    pass

# --- Database Migrations (for initial setup) ---

def apply_migrations():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                username VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                last_login_at TIMESTAMP,
                failed_login_attempts INTEGER DEFAULT 0,
                account_locked_until TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS password_reset_tokens (
                token_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID NOT NULL REFERENCES users(user_id),
                token_hash VARCHAR(255) NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cur.close()
        print("Database migrations applied successfully.")
    except Exception as e:
        print(f"Error applying database migrations: {e}")
    finally:
        if conn:
            conn.close()

# Apply migrations on startup
with app.app_context():
    apply_migrations()

# --- Routes ---

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id, password_hash, failed_login_attempts, account_locked_until FROM users WHERE username = %s", (username,))
        user_record = cur.fetchone()

        if user_record:
            user_id, stored_password_hash, failed_attempts, account_locked_until = user_record

            if account_locked_until and account_locked_until > datetime.now():
                return jsonify({"message": "Account locked. Please try again later."}), 403

            if verify_password(password, stored_password_hash):
                # Successful login
                session_id = set_session(user_id)
                cur.execute("UPDATE users SET last_login_at = CURRENT_TIMESTAMP, failed_login_attempts = 0 WHERE user_id = %s", (user_id,))
                conn.commit()
                return jsonify({"message": "Login successful", "session_id": session_id}), 200
            else:
                # Failed login attempt
                new_failed_attempts = failed_attempts + 1
                lock_until = None
                if new_failed_attempts >= 5: # Brute-force protection: Lock account after 5 failed attempts
                    lock_until = datetime.now() + timedelta(minutes=15) # Lock for 15 minutes
                    cur.execute("UPDATE users SET failed_login_attempts = %s, account_locked_until = %s WHERE user_id = %s", (new_failed_attempts, lock_until, user_id))
                else:
                    cur.execute("UPDATE users SET failed_login_attempts = %s WHERE user_id = %s", (new_failed_attempts, user_id))
                conn.commit()
                return jsonify({"message": "Invalid username or password"}), 401
        else:
            # User not found, but return generic message to prevent enumeration
            return jsonify({"message": "Invalid username or password"}), 401
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({"message": "An internal server error occurred"}), 500
    finally:
        if conn:
            conn.close()

@app.route("/logout", methods=["POST"])
def logout():
    session_id = request.headers.get("Authorization") # Assuming session_id is passed in Authorization header
    if session_id:
        delete_session(session_id)
        return jsonify({"message": "Logged out successfully"}), 200
    return jsonify({"message": "No active session"}), 400

@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"message": "Email is required"}), 400

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        user_record = cur.fetchone()

        if user_record:
            user_id = user_record[0]
            reset_token = str(uuid.uuid4())
            token_hash = hash_password(reset_token) # Hash the token before storing
            expires_at = datetime.now() + timedelta(minutes=15) # Token valid for 15 minutes

            cur.execute("INSERT INTO password_reset_tokens (user_id, token_hash, expires_at) VALUES (%s, %s, %s)",
                        (user_id, token_hash, expires_at))
            conn.commit()

            send_password_reset_email(email, reset_token) # Send the actual token (unhashed)
            return jsonify({"message": "Password reset link sent to your email"}), 200
        else:
            return jsonify({"message": "If an account with that email exists, a password reset link has been sent."}), 200 # Generic message
    except Exception as e:
        print(f"Forgot password error: {e}")
        return jsonify({"message": "An internal server error occurred"}), 500
    finally:
        if conn:
            conn.close()

@app.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    email = data.get("email")
    token = data.get("token")
    new_password = data.get("new_password")

    if not all([email, token, new_password]):
        return jsonify({"message": "Email, token, and new password are required"}), 400

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Find user by email
        cur.execute("SELECT user_id FROM users WHERE email = %s", (email,))
        user_record = cur.fetchone()
        if not user_record:
            return jsonify({"message": "Invalid or expired token"}), 400
        user_id = user_record[0]

        # Find valid reset token for the user
        cur.execute("SELECT token_hash, expires_at FROM password_reset_tokens WHERE user_id = %s AND expires_at > CURRENT_TIMESTAMP ORDER BY created_at DESC LIMIT 1", (user_id,))
        token_record = cur.fetchone()

        if token_record:
            stored_token_hash, expires_at = token_record
            if verify_password(token, stored_token_hash) and expires_at > datetime.now():
                # Token is valid, update password
                new_password_hash = hash_password(new_password)
                cur.execute("UPDATE users SET password_hash = %s, updated_at = CURRENT_TIMESTAMP WHERE user_id = %s", (new_password_hash, user_id))
                # Invalidate all reset tokens for this user after use
                cur.execute("DELETE FROM password_reset_tokens WHERE user_id = %s", (user_id,))
                conn.commit()
                return jsonify({"message": "Password reset successfully"}), 200
            else:
                return jsonify({"message": "Invalid or expired token"}), 400
        else:
            return jsonify({"message": "Invalid or expired token"}), 400
    except Exception as e:
        print(f"Reset password error: {e}")
        return jsonify({"message": "An internal server error occurred"}), 500
    finally:
        if conn:
            conn.close()

# Example route for testing session (requires a valid session_id in Authorization header)
@app.route("/protected", methods=["GET"])
def protected_route():
    session_id = request.headers.get("Authorization")
    if not session_id:
        return jsonify({"message": "Unauthorized"}), 401

    user_id = get_user_id_from_session(session_id)
    if user_id:
        return jsonify({"message": f"Welcome, user {user_id.decode()}! This is a protected resource."}), 200
    return jsonify({"message": "Invalid or expired session"}), 401

if __name__ == "__main__":
    app.run(debug=True)
