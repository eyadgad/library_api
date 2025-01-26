from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_swagger_ui import get_swaggerui_blueprint 

db = SQLAlchemy() 
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    app = Flask(__name__)
    
    # Configurations
    app.config.from_pyfile('../config.py')

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    # Swagger setup
    swaggerui_blueprint = get_swaggerui_blueprint(
        '/api/docs', 
        '/static/swagger.json',  # Swagger specification file
        config={'app_name': "Library API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix='/api/docs')

    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.graphql import graphql_bp
    app.register_blueprint(graphql_bp)

    return app
