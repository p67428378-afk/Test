import os
import uuid
from werkzeug.utils import secure_filename
from ..config import Config

class DocumentService:
    UPLOAD_FOLDER = 'uploads' # Local folder for simulation

    def __init__(self):
        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)

    def upload_document(self, file_stream, filename):
        # In a real application, this would upload to S3.
        # For now, simulate local storage.
        secured_filename = secure_filename(filename)
        unique_filename = f"{uuid.uuid4()}_{secured_filename}"
        file_path = os.path.join(self.UPLOAD_FOLDER, unique_filename)
        
        # Simulate saving the file
        with open(file_path, 'wb') as f:
            f.write(file_stream.read())
        
        # Return a simulated S3 URL or local path
        return f"s3://{Config.S3_BUCKET_NAME}/{unique_filename}"

    def get_document_url(self, file_path):
        # In a real application, this would generate a pre-signed S3 URL.
        # For now, just return the stored path.
        return file_path
