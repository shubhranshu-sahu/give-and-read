from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

import json

with open('config.json', 'r') as c:
    config = json.load(c)
    params = config["params"]
    social = config["social"]

db = SQLAlchemy() # globally creating it , to use it later

def create_app():
    app = Flask(__name__)
    
    
    @app.context_processor
    def inject_globals():
        return {
            'social_links': social,
            'params': params
        }


    load_dotenv()
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    
    db.init_app(app) # used instead of db = SQLAlchemy(app)
  
    
    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.sell import sell_bp
    from .routes.profile import profile_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(sell_bp)
    app.register_blueprint(profile_bp)

    return app
