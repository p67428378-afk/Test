from flask import request, jsonify, current_app
from . import create_app, db
from .services.loan_service import LoanService
from .services.document_service import DocumentService
from .models import Applicant, LoanApplication, Document

app = create_app()
document_service = DocumentService()

@app.route('/applications', methods=['POST'])
def submit_application():
    data = request.form.to_dict()
    files = request.files

    applicant_data = {
        'first_name': data.get('first_name'),
        'last_name': data.get('last_name'),
        'email': data.get('email'),
        'phone_number': data.get('phone_number'),
        'address': data.get('address')
    }

    application_data = {
        'loan_amount': float(data.get('loan_amount')) if data.get('loan_amount') else None,
        'loan_term_months': int(data.get('loan_term_months')) if data.get('loan_term_months') else None
    }

    document_data = []
    for key, file in files.items():
        if file.filename:
            # Simulate document upload and get a path/URL
            file_path = document_service.upload_document(file, file.filename)
            document_data.append({'document_type': key, 'file_path': file_path})

    application, error = LoanService.create_loan_application(applicant_data, application_data, document_data)

    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'Application submitted successfully',
        'reference_number': application.reference_number,
        'status': application.status
    }), 201

@app.route('/applications/<string:reference_number>', methods=['GET'])
def get_application_status(reference_number):
    status, error = LoanService.get_application_status(reference_number)
    if error:
        return jsonify({'error': error}), 404
    return jsonify({'reference_number': reference_number, 'status': status}), 200

@app.route('/applicants/<int:applicant_id>/applications', methods=['GET'])
def get_applicant_applications(applicant_id):
    applications = LoanService.get_applicant_applications(applicant_id)
    if not applications:
        return jsonify({'message': 'No applications found for this applicant'}), 404
    
    result = []
    for app in applications:
        result.append({
            'reference_number': app.reference_number,
            'status': app.status,
            'loan_amount': app.loan_amount,
            'application_date': app.application_date.isoformat()
        })
    return jsonify(result), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
