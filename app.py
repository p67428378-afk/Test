import os
import uuid
from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import Flask, make_response, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "super-secret-key")

# In-memory user store (for demonstration purposes)
# In a real application, this would be a database
USERS = {
    "test@example.com": {
        "password_hash": generate_password_hash("password123"),
        "user_id": "user-123",
        "failed_login_attempts": 0,
        "last_login_at": None,
    }
}

# In-memory session store (for demonstration purposes)
# In a real application, this would be Redis or a similar session store
SESSIONS = {}

SESSION_EXPIRATION_DAYS = 7
MAX_FAILED_LOGIN_ATTEMPTS = 5
LOGIN_RATE_LIMIT_SECONDS = 300  # 5 minutes


@app.before_request
def check_session():
    session_id = request.cookies.get("session_id")
    if session_id and session_id in SESSIONS:
        session = SESSIONS[session_id]
        if datetime.now() < session["expires_at"]:
            # Update last accessed time to extend session
            session["last_accessed_at"] = datetime.now()
            session["expires_at"] = datetime.now() + timedelta(
                days=SESSION_EXPIRATION_DAYS
            )
            request.user = session["user_id"]
        else:
            # Session expired
            del SESSIONS[session_id]
            response = make_response(redirect(url_for("login")))
            response.set_cookie("session_id", "", expires=0)
            return response
    elif request.path not in [url_for("login"), url_for("static", filename="style.css")] and not request.path.startswith('/static/') and request.endpoint != 'login_post':
        return redirect(url_for("login"))


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html", error=None)


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = USERS.get(email)

    if user:
        # Rate limiting check
        if (
            user["failed_login_attempts"] >= MAX_FAILED_LOGIN_ATTEMPTS
            and user["last_login_at"]
            and (datetime.now() - user["last_login_at"]).total_seconds()
            < LOGIN_RATE_LIMIT_SECONDS
        ):
            error_message = (
                "Too many failed login attempts. Please try again later."
            )
            return render_template("login.html", error=error_message)

        if check_password_hash(user["password_hash"], password):
            # Reset failed login attempts on successful login
            user["failed_login_attempts"] = 0
            user["last_login_at"] = datetime.now()

            session_id = str(uuid.uuid4())
            expires_at = datetime.now() + timedelta(days=SESSION_EXPIRATION_DAYS)
            SESSIONS[session_id] = {
                "user_id": user["user_id"],
                "expires_at": expires_at,
                "created_at": datetime.now(),
                "last_accessed_at": datetime.now(),
            }

            response = make_response(redirect(url_for("welcome")))
            response.set_cookie(
                "session_id",
                session_id,
                httponly=True,
                secure=True,
                samesite="Lax",
                expires=expires_at,
            )
            return response
        else:
            user["failed_login_attempts"] += 1
            user["last_login_at"] = datetime.now()
    else:
        # To prevent enumeration attacks, we don't distinguish between invalid email and password
        pass

    error_message = "Invalid email or password."
    return render_template("login.html", error=error_message)


@app.route("/welcome")
def welcome():
    if not hasattr(request, "user") or not request.user:
        return redirect(url_for("login"))
    return render_template("welcome.html", user_id=request.user)


@app.route("/logout")
def logout():
    session_id = request.cookies.get("session_id")
    if session_id and session_id in SESSIONS:
        del SESSIONS[session_id]
    response = make_response(redirect(url_for("login")))
    response.set_cookie("session_id", "", expires=0)
    return response


if __name__ == "__main__":
    app.run(debug=True)
