import uuid
from datetime import datetime
from .. import db
from ..models import LoanApplication, Applicant, Document

class LoanService:
    @staticmethod
    def create_loan_application(applicant_data, application_data, document_data):
        # Basic validation
        if not all([applicant_data.get('email'), applicant_data.get('first_name'),
                      application_data.get('loan_amount'), application_data.get('loan_term_months')]):
            return None, "Missing required application data"

        # Check if applicant already exists or create new
        applicant = Applicant.query.filter_by(email=applicant_data['email']).first()
        if not applicant:
            applicant = Applicant(
                first_name=applicant_data['first_name'],
                last_name=applicant_data.get('last_name'),
                email=applicant_data['email'],
                phone_number=applicant_data.get('phone_number'),
                address=applicant_data.get('address')
            )
            db.session.add(applicant)
            db.session.commit() # Commit to get applicant.id

        reference_number = str(uuid.uuid4())
        new_application = LoanApplication(
            applicant_id=applicant.id,
            loan_amount=application_data['loan_amount'],
            loan_term_months=application_data['loan_term_months'],
            status='Pending Review',
            reference_number=reference_number
        )
        db.session.add(new_application)
        db.session.commit() # Commit to get new_application.id

        # Handle documents (assuming document_data is a list of dicts with 'document_type' and 'file_path')
        if document_data:
            for doc in document_data:
                new_document = Document(
                    loan_application_id=new_application.id,
                    document_type=doc['document_type'],
                    file_path=doc['file_path'] # This would be an S3 URL in a real scenario
                )
                db.session.add(new_document)
            db.session.commit()

        return new_application, None

    @staticmethod
    def get_application_status(reference_number):
        application = LoanApplication.query.filter_by(reference_number=reference_number).first()
        if application:
            return application.status, None
        return None, "Application not found"

    @staticmethod
    def get_applicant_applications(applicant_id):
        applications = LoanApplication.query.filter_by(applicant_id=applicant_id).all()
        return applications

    @staticmethod
    def update_application_status(reference_number, new_status):
        application = LoanApplication.query.filter_by(reference_number=reference_number).first()
        if application:
            application.status = new_status
            db.session.commit()
            return application, None
        return None, "Application not found"
