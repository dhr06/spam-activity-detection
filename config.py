import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-for-development'
    DEBUG = os.environ.get('DEBUG') or True
    
    # Database configuration
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_USER = os.environ.get('DB_USER') or 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'password'
    DB_NAME = os.environ.get('DB_NAME') or 'spam_detection_db'
    
    # AI Model configuration
    MODEL_PATH = os.environ.get('MODEL_PATH') or 'models/spam_detection_model.pkl'
    THRESHOLD_SPAM = 0.7  # Confidence threshold for spam classification
    THRESHOLD_THREAT = 0.8  # Confidence threshold for threat classification
    
    # Application paths
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
    
    # API keys for external services (if needed)
    API_KEY = os.environ.get('API_KEY') or 'your-api-key-here'