import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///loan_application.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'loan-application-documents')
    S3_REGION = os.getenv('S3_REGION', 'us-east-1')
    S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
    S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
