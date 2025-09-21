import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Server configuration
    HOST = os.getenv("HOST", "localhost")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # Security configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    ALLOWED_DIRECTORIES = os.getenv("ALLOWED_DIRECTORIES", "/tmp").split(",")

settings = Settings()