import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Upload settings
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 16777216))  # 16MB default
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'doc'}
    
    # AI settings
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'groq')  # 'groq' or 'gemini'
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    
    # Dashboard storage
    DASHBOARD_FOLDER = 'dashboards'
    
    @staticmethod
    def init_app(app):
        """Initialize application with config"""
        # Create necessary folders
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.DASHBOARD_FOLDER, exist_ok=True)
