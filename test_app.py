import pytest
from app import create_app, db
from app.models import Applicant, LoanApplication, Document
import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_submit_application_success(client):
    # Simulate a file upload
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'loan_amount': '10000',
        'loan_term_months': '36'
    }
    # Flask test client requires files to be passed as a tuple (file_stream, filename)
    # For simplicity, we'll simulate an empty file for now.
    # In a real test, you'd create a BytesIO object with actual file content.
    files = {'id_proof': (b'fake_id_content', 'id_proof.pdf')}

    response = client.post('/applications', data=data, content_type='multipart/form-data', files=files)
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert 'reference_number' in response_data
    assert response_data['status'] == 'Pending Review'

    # Verify application in database
    with client.application.app_context():
        app = LoanApplication.query.filter_by(reference_number=response_data['reference_number']).first()
        assert app is not None
        assert app.applicant.email == 'john.doe@example.com'
        assert app.loan_amount == 10000.0
        assert app.documents[0].document_type == 'id_proof'

def test_get_application_status(client):
    # First, create an application to retrieve
    data = {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'jane.doe@example.com',
        'loan_amount': '5000',
        'loan_term_months': '12'
    }
    files = {'bank_statement': (b'fake_bank_content', 'bank_statement.pdf')}
    post_response = client.post('/applications', data=data, content_type='multipart/form-data', files=files)
    post_response_data = json.loads(post_response.data)
    reference_number = post_response_data['reference_number']

    # Now, get its status
    get_response = client.get(f'/applications/{reference_number}')
    assert get_response.status_code == 200
    get_response_data = json.loads(get_response.data)
    assert get_response_data['reference_number'] == reference_number
    assert get_response_data['status'] == 'Pending Review'

def test_submit_application_incomplete_data(client):
    data = {
        'first_name': 'Missing',
        'loan_amount': '10000',
        'loan_term_months': '36'
        # Missing email
    }
    response = client.post('/applications', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert 'error' in response_data
    assert response_data['error'] == 'Missing required application data'

def test_get_application_status_not_found(client):
    response = client.get('/applications/NONEXISTENTREF123')
    assert response.status_code == 404
    response_data = json.loads(response.data)
    assert 'error' in response_data
    assert response_data['error'] == 'Application not found'
