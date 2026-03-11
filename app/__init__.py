from flask import Flask 
from config import Config 
from app.site.routes import site
from app.auth.routes import auth
from app.api.routes import api

from flask_migrate import Migrate
from models import db as root_db, Login_manager, ma 
from flask_cors import CORS
from helpers import JSONEncoder


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    app.register_blueprint(site)
    app.register_blueprint(auth)
    app.register_blueprint(api)

    app.json_encoder = JSONEncoder
    root_db.init_app(app)
    Login_manager.init_app(app)
    Login_manager.login_view = 'auth.signin'
    ma.init_app(app)
    Migrate(app, root_db)
    
    # Initialize Supabase only if needed
    try:
        from flask_supabase import Supabase
        supabase_extension = Supabase(app)
    except Exception as e:
        print(f"Warning: Flask-Supabase initialization failed: {repr(e)}")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)