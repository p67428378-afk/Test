from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Customer, EmploymentDetails, LoanApplication, Document
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Setup database
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base.metadata.create_all(engine) # Create tables if they don't exist
Session = sessionmaker(bind=engine)

@app.route('/')
def hello_world():
    return 'Hello, World! This is the Loan Application Backend.'

# User Service API
@app.route('/customers', methods=['POST'])
def create_customer():
    session = Session()
    try:
        data = request.get_json()
        # Basic validation
        required_fields = ['full_name', 'dob', 'ssn', 'address', 'contact_info', 'citizenship_status']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400

        # Date of Birth validation
        try:
            dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid DOB format. Use YYYY-MM-DD'}), 400

        new_customer = Customer(
            full_name=data['full_name'],
            dob=dob,
            ssn=data['ssn'], # In a real app, this would be encrypted
            address=data['address'],
            contact_info=data['contact_info'],
            citizenship_status=data['citizenship_status'],
            has_pending_legal_cases=data.get('has_pending_legal_cases', False)
        )
        session.add(new_customer)
        session.commit()
        return jsonify({'message': 'Customer created successfully', 'customer_id': new_customer.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    session = Session()
    try:
        customer = session.query(Customer).filter_by(id=customer_id).first()
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404

        customer_data = {
            'id': customer.id,
            'full_name': customer.full_name,
            'dob': customer.dob.strftime('%Y-%m-%d'),
            'ssn': customer.ssn, # In a real app, this would be decrypted for authorized access
            'address': customer.address,
            'contact_info': customer.contact_info,
            'citizenship_status': customer.citizenship_status,
            'has_pending_legal_cases': customer.has_pending_legal_cases
        }
        return jsonify(customer_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

# Employment Service API
@app.route('/customers/<int:customer_id>/employment', methods=['POST'])
def add_employment_details(customer_id):
    session = Session()
    try:
        customer = session.query(Customer).filter_by(id=customer_id).first()
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404

        data = request.get_json()
        required_fields = ['employer_name', 'employer_address', 'job_title', 'annual_income']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400

        new_employment = EmploymentDetails(
            customer_id=customer_id,
            employer_name=data['employer_name'],
            employer_address=data['employer_address'],
            job_title=data['job_title'],
            annual_income=data['annual_income'], # Encrypted in real app
            employment_history=data.get('employment_history')
        )
        session.add(new_employment)
        session.commit()
        return jsonify({'message': 'Employment details added successfully', 'employment_id': new_employment.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@app.route('/customers/<int:customer_id>/employment', methods=['GET'])
def get_employment_details(customer_id):
    session = Session()
    try:
        employment_details = session.query(EmploymentDetails).filter_by(customer_id=customer_id).all()
        if not employment_details:
            return jsonify({'message': 'No employment details found for this customer'}), 404

        result = []
        for detail in employment_details:
            result.append({
                'id': detail.id,
                'customer_id': detail.customer_id,
                'employer_name': detail.employer_name,
                'employer_address': detail.employer_address,
                'job_title': detail.job_title,
                'annual_income': detail.annual_income, # Decrypted in real app
                'employment_history': detail.employment_history
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=True)
