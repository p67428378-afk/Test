from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Customer, EmploymentDetails, LoanApplication, Document
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Setup database
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base.metadata.create_all(engine) # Create tables if they don't exist
Session = sessionmaker(bind=engine)

@app.route('/')
def hello_world():
    return 'Hello, World! This is the Loan Application Backend.'

if __name__ == '__main__':
    app.run(debug=True)
