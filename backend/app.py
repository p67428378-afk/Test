"""
Module: app
Purpose: Flask application for Loan Application Review and Processing.
Author: Gemini
Created: 2026-03-16
Notes: Implements RESTful APIs for managing loan applications.
"""

import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel, ValidationError, Field
from typing import Optional, List

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Database Model ---
class LoanApplication(db.Model):
    """
    Represents a loan application in the system.
    """
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='Pending')  # Pending, Approved, Rejected
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    approval_date = db.Column(db.DateTime, nullable=True)
    rejection_date = db.Column(db.DateTime, nullable=True)
    rejection_reason = db.Column(db.String(500), nullable=True)
    loan_amount = db.Column(db.Float, nullable=False)
    term = db.Column(db.Integer, nullable=False)  # in months
    interest_rate = db.Column(db.Float, nullable=False)
    credit_score = db.Column(db.Integer, nullable=False)
    income = db.Column(db.Float, nullable=False)
    debt_to_income_ratio = db.Column(db.Float, nullable=False)
    reviewed_by = db.Column(db.String(100), nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'applicant_id': self.applicant_id,
            'status': self.status,
            'submission_date': self.submission_date.isoformat() if self.submission_date else None,
            'approval_date': self.approval_date.isoformat() if self.approval_date else None,
            'rejection_date': self.rejection_date.isoformat() if self.rejection_date else None,
            'rejection_reason': self.rejection_reason,
            'loan_amount': self.loan_amount,
            'term': self.term,
            'interest_rate': self.interest_rate,
            'credit_score': self.credit_score,
            'income': self.income,
            'debt_to_income_ratio': self.debt_to_income_ratio,
            'reviewed_by': self.reviewed_by,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

# --- Pydantic Models for Request Validation and Response ---
class LoanApplicationBase(BaseModel):
    applicant_id: str = Field(..., example="APL001")
    loan_amount: float = Field(..., gt=0, example=50000.0)
    term: int = Field(..., gt=0, example=60)
    interest_rate: float = Field(..., gt=0, example=4.5)
    credit_score: int = Field(..., ge=300, le=850, example=720)
    income: float = Field(..., gt=0, example=60000.0)
    debt_to_income_ratio: float = Field(..., ge=0, le=100, example=30.0)

class LoanApplicationCreate(LoanApplicationBase):
    pass

class LoanApplicationResponse(LoanApplicationBase):
    id: int
    status: str
    submission_date: datetime
    approval_date: Optional[datetime] = None
    rejection_date: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    reviewed_by: Optional[str] = None
    last_updated: datetime

    class Config:
        from_attributes = True

class ApproveRejectRequest(BaseModel):
    reviewed_by: str = Field(..., example="loan_officer_1")
    rejection_reason: Optional[str] = None # Required for rejection

# --- API Endpoints ---
@app.route('/applications', methods=['GET'])
def get_applications():
    """
    Retrieves a list of all loan applications.
    """
    applications = LoanApplication.query.all()
    return jsonify([app.to_dict() for app in applications])

@app.route('/applications/<int:app_id>', methods=['GET'])
def get_application(app_id):
    """
    Retrieves details of a specific loan application by ID.
    """
    application = LoanApplication.query.get(app_id)
    if not application:
        return jsonify({'message': 'Loan application not found'}), 404
    return jsonify(application.to_dict())

@app.route('/applications/<int:app_id>/approve', methods=['POST'])
def approve_application(app_id):
    """
    Approves a loan application.
    """
    application = LoanApplication.query.get(app_id)
    if not application:
        return jsonify({'message': 'Loan application not found'}), 404

    if application.status != 'Pending':
        return jsonify({'message': f'Application is already {application.status}'}), 400

    try:
        data = ApproveRejectRequest(**request.json)
    except ValidationError as e:
        return jsonify({'message': 'Invalid request data', 'errors': e.errors()}), 400

    # Business logic for approval criteria (example: credit score > 680, income > 40000, DTI < 40)
    if not (application.credit_score > 680 and application.income > 40000 and application.debt_to_income_ratio < 40):
        return jsonify({'message': 'Application does not meet approval criteria'}), 400

    application.status = 'Approved'
    application.approval_date = datetime.utcnow()
    application.reviewed_by = data.reviewed_by
    db.session.commit()
    return jsonify(application.to_dict()), 200

@app.route('/applications/<int:app_id>/reject', methods=['POST'])
def reject_application(app_id):
    """
    Rejects a loan application.
    """
    application = LoanApplication.query.get(app_id)
    if not application:
        return jsonify({'message': 'Loan application not found'}), 404

    if application.status != 'Pending':
        return jsonify({'message': f'Application is already {application.status}'}), 400

    try:
        data = ApproveRejectRequest(**request.json)
        if not data.rejection_reason:
            return jsonify({'message': 'Rejection reason is required'}), 400
    except ValidationError as e:
        return jsonify({'message': 'Invalid request data', 'errors': e.errors()}), 400

    application.status = 'Rejected'
    application.rejection_date = datetime.utcnow()
    application.rejection_reason = data.rejection_reason
    application.reviewed_by = data.reviewed_by
    db.session.commit()
    return jsonify(application.to_dict()), 200

@app.route('/applications', methods=['POST'])
def create_application():
    """
    Creates a new loan application. (For testing purposes, not part of LO workflow)
    """
    try:
        data = LoanApplicationCreate(**request.json)
    except ValidationError as e:
        return jsonify({'message': 'Invalid request data', 'errors': e.errors()}), 400

    new_application = LoanApplication(
        applicant_id=data.applicant_id,
        loan_amount=data.loan_amount,
        term=data.term,
        interest_rate=data.interest_rate,
        credit_score=data.credit_score,
        income=data.income,
        debt_to_income_ratio=data.debt_to_income_ratio
    )
    db.session.add(new_application)
    db.session.commit()
    return jsonify(new_application.to_dict()), 201

# --- Initialize Database (for in-memory or first run) ---
with app.app_context():
    db.create_all()
    # Seed some dummy data if the database is empty
    if not LoanApplication.query.first():
        dummy_applications = [
            LoanApplication(
                applicant_id="APL001", loan_amount=75000.0, term=120, interest_rate=3.8,
                credit_score=750, income=80000.0, debt_to_income_ratio=25.0, status="Pending"
            ),
            LoanApplication(
                applicant_id="APL002", loan_amount=30000.0, term=48, interest_rate=6.2,
                credit_score=620, income=35000.0, debt_to_income_ratio=45.0, status="Pending"
            ),
            LoanApplication(
                applicant_id="APL003", loan_amount=120000.0, term=180, interest_rate=4.1,
                credit_score=700, income=95000.0, debt_to_income_ratio=32.0, status="Pending"
            ),
            LoanApplication(
                applicant_id="APL004", loan_amount=50000.0, term=60, interest_rate=5.0,
                credit_score=690, income=55000.0, debt_to_income_ratio=38.0, status="Pending"
            ),
            LoanApplication(
                applicant_id="APL005", loan_amount=20000.0, term=36, interest_rate=7.0,
                credit_score=580, income=28000.0, debt_to_income_ratio=50.0, status="Pending"
            )
        ]
        db.session.add_all(dummy_applications)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
