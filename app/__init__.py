from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from flask_marshmallow import Marshmallow
from flask import jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.json.sort_keys = False

    db.init_app(app)
    ma.init_app(app)

    from .routes.messages import messages_bp
    app.register_blueprint(messages_bp, url_prefix="/messages")

    # Tratadores globais de erro (explicados na seção 5.6)
    register_error_handlers(app)

    return app

def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({
            "error": "Validation Error",
            "messages": error.messages
        }), 400

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({
            "error": error.name,
            "message": error.description
        }), error.code

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        return jsonify({
            "error": "Internal Server Error",
            "message": str(error)
        }), 500