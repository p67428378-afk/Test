from sqlalchemy import create_engine, Column, Integer, String, Date, Text, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(255), nullable=False)
    dob = Column(Date, nullable=False)
    ssn = Column(String(255), nullable=False)  # Encrypted
    address = Column(String(255), nullable=False)
    contact_info = Column(String(255), nullable=False)
    citizenship_status = Column(String(50), nullable=False)
    has_pending_legal_cases = Column(Boolean, default=False)

    employment_details = relationship('EmploymentDetails', back_populates='customer')
    loan_applications = relationship('LoanApplication', back_populates='customer')
    documents = relationship('Document', back_populates='customer')

    def __repr__(self):
        return f"<Customer(id={self.id}, full_name='{self.full_name}')>"

class EmploymentDetails(Base):
    __tablename__ = 'employment_details'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    employer_name = Column(String(255), nullable=False)
    employer_address = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=False)
    annual_income = Column(String(255), nullable=False)  # Encrypted
    employment_history = Column(Text, nullable=True)

    customer = relationship('Customer', back_populates='employment_details')

    def __repr__(self):
        return f"<EmploymentDetails(id={self.id}, employer_name='{self.employer_name}')>"

class LoanApplication(Base):
    __tablename__ = 'loan_applications'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    purpose = Column(String(255), nullable=False)
    loan_amount = Column(Float, nullable=False)
    application_status = Column(String(50), default='Pending')
    submission_date = Column(Date, default=datetime.utcnow)

    customer = relationship('Customer', back_populates='loan_applications')
    documents = relationship('Document', back_populates='loan_application')

    def __repr__(self):
        return f"<LoanApplication(id={self.id}, loan_amount={self.loan_amount})>"

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    loan_application_id = Column(Integer, ForeignKey('loan_applications.id'), nullable=True)
    document_type = Column(String(100), nullable=False)
    file_path = Column(String(255), nullable=False)  # Encrypted path or reference
    upload_date = Column(Date, default=datetime.utcnow)

    customer = relationship('Customer', back_populates='documents')
    loan_application = relationship('LoanApplication', back_populates='documents')

    def __repr__(self):
        return f"<Document(id={self.id}, document_type='{self.document_type}')>"
