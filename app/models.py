from datetime import datetime
from . import db

class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(200))
    # Add other personal info fields as needed

    applications = db.relationship('LoanApplication', backref='applicant', lazy=True)

    def __repr__(self):
        return f"<Applicant {self.first_name} {self.last_name}>"

class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicant.id'), nullable=False)
    loan_amount = db.Column(db.Float, nullable=False)
    loan_term_months = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='Pending Review', nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    reference_number = db.Column(db.String(100), unique=True, nullable=False)
    # Add other financial info fields as needed

    documents = db.relationship('Document', backref='loan_application', lazy=True)

    def __repr__(self):
        return f"<LoanApplication {self.reference_number} - {self.status}>"

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_application_id = db.Column(db.Integer, db.ForeignKey('loan_application.id'), nullable=False)
    document_type = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(255), nullable=False) # S3 URL or local path
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Document {self.document_type} for Application {self.loan_application_id}>"
