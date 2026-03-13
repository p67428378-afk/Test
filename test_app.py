import pytest
from app import app, USERS, SESSIONS
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'<h2>Login</h2>' in response.data

def test_successful_login(client):
    # Ensure the test user exists and has the correct password hash
    USERS['test@example.com'] = {
        'password_hash': generate_password_hash('password123'),
        'user_id': 'user-123',
        'failed_login_attempts': 0,
        'last_login_at': None,
    }
    SESSIONS.clear() # Clear sessions before test

    response = client.post('/login', data={'email': 'test@example.com', 'password': 'password123'})
    assert response.status_code == 302  # Redirect to welcome page
    assert '/welcome' in response.headers['Location']
    assert 'session_id' in response.headers['Set-Cookie']

def test_invalid_password_login(client):
    USERS['test@example.com'] = {
        'password_hash': generate_password_hash('password123'),
        'user_id': 'user-123',
        'failed_login_attempts': 0,
        'last_login_at': None,
    }
    SESSIONS.clear()

    response = client.post('/login', data={'email': 'test@example.com', 'password': 'wrongpassword'})
    assert response.status_code == 200  # Stays on login page
    assert b'Invalid email or password.' in response.data
    assert 'session_id' not in response.headers.get('Set-Cookie', '')

def test_non_existent_user_login(client):
    SESSIONS.clear()
    response = client.post('/login', data={'email': 'nonexistent@example.com', 'password': 'anypassword'})
    assert response.status_code == 200
    assert b'Invalid email or password.' in response.data
    assert 'session_id' not in response.headers.get('Set-Cookie', '')

def test_access_welcome_unauthenticated(client):
    SESSIONS.clear()
    response = client.get('/welcome')
    assert response.status_code == 302  # Redirect to login
    assert '/login' in response.headers['Location']

def test_access_welcome_authenticated(client):
    # Manually create a session
    session_id = 'test-session-id'
    user_id = 'user-123'
    SESSIONS[session_id] = {
        'user_id': user_id,
        'expires_at': datetime.now() + timedelta(days=7),
        'created_at': datetime.now(),
        'last_accessed_at': datetime.now(),
    }

    response = client.get('/welcome', headers={'Cookie': f'session_id={session_id}'})
    assert response.status_code == 200
    assert f'Welcome, {user_id}!' in response.get_data(as_text=True)

def test_logout(client):
    # First, log in to get a session
    USERS['test@example.com'] = {
        'password_hash': generate_password_hash('password123'),
        'user_id': 'user-123',
        'failed_login_attempts': 0,
        'last_login_at': None,
    }
    SESSIONS.clear()
    login_response = client.post('/login', data={'email': 'test@example.com', 'password': 'password123'})
    session_cookie = login_response.headers['Set-Cookie']

    # Then, logout
    response = client.get('/logout', headers={'Cookie': session_cookie})
    assert response.status_code == 302  # Redirect to login
    assert '/login' in response.headers['Location']
    assert 'session_id=""; Expires=Thu, 01 Jan 1970 00:00:00 GMT' in response.headers['Set-Cookie']
    # Verify session is removed from SESSIONS (this is a simplified check)
    # In a real app, you'd check if the session ID is no longer valid
    assert not SESSIONS # Assuming only one session was active
