import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config():
    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY is required but missing!")
    
    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
    
    DATABASE_URI = os.getenv("DATABASE_URI")
    if not DATABASE_URI:
        raise ValueError("DATABASE_URI is missing!")

    SQLALCHEMY_DATABASE_URI = DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    DEBUG = True


# Initialize Supabase client lazily (deferred initialization)
_supabase_client = None

def get_supabase_client():
    """Get Supabase client, initializing it if needed."""
    global _supabase_client
    if _supabase_client is None:
        try:
            from supabase import create_client, Client
            _supabase_client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
            print("Supabase client initialized successfully!")
        except Exception as e:
            print(f"Warning: Failed to initialize Supabase client: {repr(e)}")
            # Return None instead of raising, allows app to run without Supabase
            _supabase_client = False
    return _supabase_client if _supabase_client else None


def test_supabase():
    """Test the Supabase connection."""
    try:
        client = get_supabase_client()
        if client:
            response = client.table("test").select("*").execute()
            print("Supabase Test Query Successful:", response)
        else:
            print("Supabase client not available")
    except Exception as e:
        print("Supabase Test Query Failed:", repr(e))